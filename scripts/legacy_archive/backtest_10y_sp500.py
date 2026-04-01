import yfinance as yf
import pandas as pd
import json

# Representative S&P 500 Growth/Volatility Universe
SYMBOLS = ["NVDA", "AMD", "META", "GOOGL", "AMZN", "MSFT", "ADBE", "CRM", "NFLX", "COST", 
           "AVGO", "INTU", "SNOW", "DDOG", "CRWD", "MDB", "PANW", "FTNT", "ZS", "VRTX"]

def run_10y_audit(symbol):
    try:
        df = yf.Ticker(symbol).history(period="10y")
        if len(df) < 500: return []
        
        # Indicators
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = delta.clip(upper=0).abs()
        rsi = 100 - (100 / (1 + (gain.rolling(14).mean() / loss.rolling(14).mean())))
        
        vectors = []
        for i in range(200, len(df) - 10):
            # 1. Structural Trend: Price > 200 SMA
            if df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. NEW EXCLUSION RULES
            if rsi.iloc[i] > 65: continue # RSI Ceiling
            if (df['Close'].iloc[i] / df['SMA50'].iloc[i] - 1) > 0.08: continue # SMA Stretch Ceiling
            
            # 3. Institutional Footprint
            vol_parity = df['Volume'].iloc[i] / df['VolMA20'].iloc[i]
            atr_ratio = df['ATR14'].iloc[i] / df['Close'].iloc[i]
            
            if 0.9 <= vol_parity <= 1.1 and 0.02 <= atr_ratio <= 0.04:
                # Vector Logic (7-day holding return)
                ret = ((df['Close'].iloc[i+7] / df['Close'].iloc[i]) - 1) * 100
                vectors.append({"date": str(df.index[i].date()), "return": round(ret, 2)})
        return vectors
    except: return []

final_report = {}
for sym in SYMBOLS:
    final_report[sym] = run_10y_audit(sym)

print(json.dumps(final_report, indent=4))
