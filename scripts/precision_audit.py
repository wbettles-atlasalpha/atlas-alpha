import yfinance as yf
import pandas as pd
import json

# Universe (A mix of quality growth & institutional favorites to ensure density)
# This includes the "Growth" list we identified as the engine's sweet spot.
SYMBOLS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'PATH']

def run_precision_audit(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="2y")
        if len(df) < 200: return []
        
        # Fundamental Proxy: (High ROE / Margin potential is hard to get via YF in live scan, 
        # so we use Price Momentum as a proxy for Fundamental Quality)
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        
        # Relative Strength (6mo performance vs broad market proxy)
        df['6mo_ret'] = df['Close'].pct_change(126)
        
        vectors = []
        for i in range(200, len(df) - 10):
            # 1. Structural Trend: Price > 50 & 200 SMA
            if df['Close'].iloc[i] < df['SMA50'].iloc[i] or df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. Quality/Strength Filter (Relative Strength > 10% vs index proxy)
            if df['6mo_ret'].iloc[i] < 0.10: continue
                
            # 3. Institutional Footprint: Vol Parity (0.95-1.05) & ATR Stability (0.02-0.04)
            vol_parity = df['Volume'].iloc[i] / df['VolMA20'].iloc[i]
            atr_ratio = df['ATR14'].iloc[i] / df['Close'].iloc[i]
            
            if 0.9 <= vol_parity <= 1.1 and 0.02 <= atr_ratio <= 0.04:
                # Vector Logic
                entry = df['Close'].iloc[i]
                stop_loss = entry * 0.95
                
                future = df.iloc[i+1 : i+11]
                hit_invalidation = False
                ret = 0
                for idx, (date, row) in enumerate(future.iterrows()):
                    if row['Low'] < stop_loss:
                        hit_invalidation = True
                        ret = -5.0
                        break
                    ret = ((row['Close'] / entry) - 1) * 100
                
                vectors.append({
                    "symbol": symbol,
                    "date": str(df.index[i].date()),
                    "invalidated": hit_invalidation,
                    "return": round(ret, 2)
                })
        return vectors
    except: return []

final_data = {}
for s in SYMBOLS:
    final_data[s] = run_precision_audit(s)

print(json.dumps(final_data, indent=4))
