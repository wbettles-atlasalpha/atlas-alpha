import yfinance as yf
import pandas as pd
import numpy as np
import json

# Growth Tickers
GROWTH_TICKERS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET']

def scan_growth_vcp_v2(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start="2025-01-01", end="2025-12-31")
        if len(df) < 200: return []
        
        # Indicators
        df['SMA200'] = df['Close'].rolling(window=200).mean()
        df['VolMA20'] = df['Volume'].rolling(window=20).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(window=14).mean()
        
        vectors = []
        
        for i in range(200, len(df)):
            # 1. Structural Uptrend
            if df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. Volatility Contraction (ATR < 7% of Close)
            # 3. Trigger (Breakout Volume > 110%)
            if (df['ATR14'].iloc[i] / df['Close'].iloc[i]) < 0.07:
                if df['Volume'].iloc[i] > (1.1 * df['VolMA20'].iloc[i]):
                     vectors.append({"symbol": symbol, "date": str(df.index[i].date()), "price": round(df['Close'].iloc[i], 2)})
        return vectors
    except:
        return []

all_vectors = []
for sym in GROWTH_TICKERS:
    found = scan_growth_vcp_v2(sym)
    all_vectors.extend(found)
    print(f"{sym}: {len(found)} vectors")
    
print(f"Total Vectors Found: {len(all_vectors)}")
print(json.dumps(all_vectors, indent=4))
