import yfinance as yf
import pandas as pd
import numpy as np

# Nasdaq Tickers
NASDAQ_TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "META", "GOOGL", "AVGO", "TSLA", "COST", "PEP", "ADBE", "AMD", "NFLX", "INTC", "CSCO", "CMCSA", "AMGN", "HON", "TXN", "QCOM", "TMUS", "INTU", "SBUX", "GILD", "MDLZ", "BKNG", "ADP", "VRTX", "MU", "REGN"]

def scan_vcp(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start="2025-01-01", end="2025-12-31")
        
        # Indicators
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        df['EMA200'] = df['Close'].ewm(span=200).mean()
        df['VolMA20'] = df['Volume'].rolling(window=20).mean()
        df['TR'] = np.maximum(df['High'] - df['Low'], np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))))
        df['ATR14'] = df['TR'].rolling(window=14).mean()
        
        vectors = 0
        
        for i in range(200, len(df) - 5):
            # 1. Uptrend Condition
            if df['Close'].iloc[i] < df['EMA50'].iloc[i] or df['Close'].iloc[i] < df['EMA200'].iloc[i]:
                continue
            
            # 2. Consolidation Window (7-14 days)
            # Check if volume is consistently < 50% of 20-day MA for 7 days
            if i > 15:
                vol_window = df['Volume'].iloc[i-7:i]
                if all(vol_window < (0.5 * df['VolMA20'].iloc[i])):
                    # 3. Vector Trigger (Breakout)
                    if df['Volume'].iloc[i] > (1.5 * df['VolMA20'].iloc[i]):
                        if df['Close'].iloc[i] > df['High'].iloc[i-7:i].max():
                            vectors += 1
        return vectors
    except:
        return 0

total_vectors = 0
for sym in NASDAQ_TICKERS:
    count = scan_vcp(sym)
    total_vectors += count
    
print(f"Total Vectors Found: {total_vectors}")
