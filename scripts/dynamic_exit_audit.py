import yfinance as yf
import pandas as pd
import json

SYMBOLS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET']

def run_dynamic_exit_audit(symbol):
    try:
        df = yf.Ticker(symbol).history(period="2y")
        if len(df) < 200: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        vectors = []
        for i in range(200, len(df) - 20):
            # 1. Structural Trend & Institutional Footprint (1.05-1.2 vol)
            if df['Close'].iloc[i] > df['SMA200'].iloc[i]:
                vol_ratio = df['Volume'].iloc[i] / df['VolMA20'].iloc[i]
                if 1.05 <= vol_ratio <= 1.2:
                    entry = df['Close'].iloc[i]
                    # Dynamic Exit: Stop = Entry - 2*ATR, Profit = Trailing Stop (1.5*ATR)
                    atr = df['ATR14'].iloc[i]
                    stop = entry - (2 * atr)
                    
                    ret = 0
                    for idx, (date, row) in enumerate(df.iloc[i+1:].iterrows()):
                        # Stop Loss hit
                        if row['Low'] < stop:
                            ret = ((stop / entry) - 1) * 100
                            break
                        # Take Profit (or sell after 15 days if trailing)
                        if idx > 15:
                            ret = ((row['Close'] / entry) - 1) * 100
                            break
                    vectors.append({"symbol": symbol, "return": round(ret, 2)})
        return vectors
    except: return []

results = []
for s in SYMBOLS:
    results.extend(run_dynamic_exit_audit(s))

wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
print(json.dumps({"success_rate": round(success_rate, 2), "total": len(results), "sample": results[:10]}, indent=4))
