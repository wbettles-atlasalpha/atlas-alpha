import yfinance as yf
import pandas as pd
import numpy as np

NASDAQ_TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "META", "GOOGL", "AVGO", "TSLA", "COST", "PEP"]

def scan_vcp(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start="2025-01-01", end="2025-12-31")
        
        # Indicators
        df['VolMA20'] = df['Volume'].rolling(window=20).mean()
        
        vectors = 0
        
        for i in range(20, len(df)):
            # Relaxed constraint: Vol < 80% of MA
            vol_window = df['Volume'].iloc[i-7:i]
            if all(vol_window < (0.8 * df['VolMA20'].iloc[i])):
                # Breakout Volume > 120%
                if df['Volume'].iloc[i] > (1.2 * df['VolMA20'].iloc[i]):
                     vectors += 1
        return vectors
    except:
        return 0

total_vectors = 0
for sym in NASDAQ_TICKERS:
    count = scan_vcp(sym)
    total_vectors += count
    
print(f"Total Vectors Found: {total_vectors}")
