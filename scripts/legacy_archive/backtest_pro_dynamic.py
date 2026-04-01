import yfinance as yf
import pandas as pd
import json

# Universe
UNIVERSE = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "BHP.AX", "CBA.AX", "CSL.AX"]

def run_dynamic_backtest(symbol):
    try:
        df = yf.Ticker(symbol).history(start="2023-01-01", end="2025-12-31")
        if len(df) < 200: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        
        vectors = []
        for i in range(200, len(df) - 30):
            # VCP Pattern: Volatility Contraction + Volume Drought
            if (df['ATR14'].iloc[i] / df['Close'].iloc[i]) < 0.05:
                if df['Volume'].iloc[i-3:i].mean() < (0.8 * df['VolMA20'].iloc[i]):
                    if df['Volume'].iloc[i] > (1.2 * df['VolMA20'].iloc[i]):
                        # Vector Found
                        entry = df['Close'].iloc[i]
                        stop_loss = entry * 0.95
                        atr = df['ATR14'].iloc[i]
                        
                        # Dynamic Exit Logic
                        final_ret = 0
                        invalidated = False
                        
                        for idx, (date, row) in enumerate(df.iloc[i+1:].iterrows()):
                            # Stop Loss
                            if row['Low'] < stop_loss:
                                invalidated = True
                                final_ret = -5.0
                                break
                            
                            # Trailing Profit: Exit if price drops 2x ATR from high
                            # (Simplified logic for backtest)
                            if row['Close'] < (row['High'] - (2 * atr)):
                                final_ret = ((row['Close'] / entry) - 1) * 100
                                break
                        
                        vectors.append({"symbol": symbol, "date": str(df.index[i].date()), "invalidated": invalidated, "return": round(final_ret, 2)})
        return vectors
    except: return []

results = {}
for sym in UNIVERSE:
    results[sym] = run_dynamic_backtest(sym)

print(json.dumps(results, indent=4))
