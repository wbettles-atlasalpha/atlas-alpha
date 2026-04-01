import yfinance as yf
import pandas as pd
import json

# Universe
SYMBOLS = ['NVDA', 'CRWD', 'DDOG', 'MDB', 'NET', 'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD']

def run_backtest(symbol):
    try:
        df = yf.Ticker(symbol).history(start="2025-01-01", end="2025-12-31")
        if len(df) < 200: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        vectors = []
        for i in range(200, len(df) - 10):
            # 1. Structural Trend: Price > SMA200
            if df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. Institutional Footprint: Volume > 130% MA
            if df['Volume'].iloc[i] > (1.3 * df['VolMA20'].iloc[i]):
                # 3. Success Logic: Price 10 days later
                ret = ((df['Close'].iloc[i+10] / df['Close'].iloc[i]) - 1) * 100
                vectors.append({"return": round(ret, 2)})
        return vectors
    except: return []

results = []
for s in SYMBOLS:
    results.extend(run_backtest(s))

wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
avg_ret = sum([r['return'] for r in results]) / len(results) if len(results) > 0 else 0

print(json.dumps({"success_rate": round(success_rate, 2), "avg_return": round(avg_ret, 2), "total_vectors": len(results)}, indent=4))
