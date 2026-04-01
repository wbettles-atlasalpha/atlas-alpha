import yfinance as yf
import pandas as pd
import numpy as np

# Growth Tickers
GROWTH_TICKERS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET']

def scan_growth_vcp(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start="2025-01-01", end="2025-12-31")
        if len(df) < 200: return 0
        
        # Indicators
        df['SMA200'] = df['Close'].rolling(window=200).mean()
        df['VolMA20'] = df['Volume'].rolling(window=20).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(window=14).mean()
        
        vectors = 0
        
        for i in range(200, len(df) - 5):
            # 1. Structural Uptrend
            if df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. Volatility Contraction (ATR < 3% of Close)
            if (df['ATR14'].iloc[i] / df['Close'].iloc[i]) > 0.03: continue
                
            # 3. Volume Drought (5-day vol < 90% MA20)
            vol_window = df['Volume'].iloc[i-5:i]
            if all(vol_window < (0.9 * df['VolMA20'].iloc[i])):
                
                # 4. Trigger (Breakout Volume > 130%)
                if df['Volume'].iloc[i] > (1.3 * df['VolMA20'].iloc[i]):
                     vectors += 1
        return vectors
    except:
        return 0

total_vectors = 0
for sym in GROWTH_TICKERS:
    count = scan_growth_vcp(sym)
    total_vectors += count
    print(f"{sym}: {count} vectors")
    
print(f"Total Vectors Found: {total_vectors}")
