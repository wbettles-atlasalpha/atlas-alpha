import yfinance as yf
import pandas as pd
import json

# Testing a broad set
UNIVERSE = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "AVGO", "TSLA", "COST", "PEP", "XRO.AX", "PME.AX", "WBT.AX", "NST.AX", "MIN.AX"]

def backtest_parity(sym):
    try:
        df = yf.Ticker(sym).history(start="2023-01-01", end="2025-12-31")
        if len(df) < 200: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        
        results = []
        for i in range(200, len(df) - 10):
            # Strict logic:
            # 1. Uptrend
            # 2. Volume Parity (0.9 to 1.1)
            # 3. ATR Stability (0.02 to 0.04)
            if df['Close'].iloc[i] > df['SMA200'].iloc[i]:
                vol_parity = df['Volume'].iloc[i] / df['VolMA20'].iloc[i]
                atr_ratio = df['ATR14'].iloc[i] / df['Close'].iloc[i]
                
                if 0.9 <= vol_parity <= 1.1 and 0.02 <= atr_ratio <= 0.04:
                    # Vector Found: Log return 10 days later
                    ret = ((df['Close'].iloc[i+10] / df['Close'].iloc[i]) - 1) * 100
                    results.append({"symbol": sym, "return": round(ret, 2)})
        return results
    except: return []

final_report = {}
for s in UNIVERSE:
    final_report[s] = backtest_parity(s)

print(json.dumps(final_report, indent=4))
