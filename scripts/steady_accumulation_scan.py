import yfinance as yf
import pandas as pd
import json

# Universe
SYMBOLS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'PATH']

def run_steady_scan(symbol):
    try:
        df = yf.Ticker(symbol).history(period="2y")
        if len(df) < 200: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = delta.clip(upper=0).abs()
        df['RSI'] = 100 - (100 / (1 + (gain.rolling(14).mean() / loss.rolling(14).mean())))
        
        vectors = []
        for i in range(200, len(df) - 10):
            # 1. Structural Trend: Price > SMA200
            if df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. RSI Sweet Spot (45-60) - Avoids Overbought/Oversold
            if not (45 <= df['RSI'].iloc[i] <= 60): continue
            
            # 3. Steady Accumulation (Volume 1.05-1.2x MA) - NOT "Blow-off"
            vol_ratio = df['Volume'].iloc[i] / df['VolMA20'].iloc[i]
            if 1.05 <= vol_ratio <= 1.2:
                # Execution Logic (Target 10-day hold)
                entry = df['Close'].iloc[i]
                target_ret = ((df['Close'].iloc[i+10] / entry) - 1) * 100
                vectors.append({"symbol": symbol, "date": str(df.index[i].date()), "return": round(target_ret, 2)})
        return vectors
    except: return []

results = []
for s in SYMBOLS:
    results.extend(run_steady_scan(s))

wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
print(json.dumps({"success_rate": round(success_rate, 2), "total": len(results), "sample": results[:10]}, indent=4))
