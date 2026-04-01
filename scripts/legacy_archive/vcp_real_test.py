import yfinance as yf
import pandas as pd
import json

SYMBOLS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET']

def run_vcp_audit(symbol):
    try:
        df = yf.Ticker(symbol).history(period="2y")
        if len(df) < 200: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        # VCP logic: 5 days of decreasing volume (drought) followed by a 1-day spike
        df['Vol_Trend'] = df['Volume'].diff()
        
        vectors = []
        for i in range(20, len(df) - 10):
            # 1. Volume Drought (Consecutive lower volume days)
            if all(df['Volume'].iloc[i-5:i] < df['VolMA20'].iloc[i-5:i]):
                # 2. Volume Spike
                if df['Volume'].iloc[i] > (1.3 * df['VolMA20'].iloc[i]):
                    ret = ((df['Close'].iloc[i+10] / df['Close'].iloc[i]) - 1) * 100
                    vectors.append({"symbol": symbol, "return": round(ret, 2)})
        return vectors
    except: return []

results = []
for s in SYMBOLS:
    results.extend(run_vcp_audit(s))

wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
print(json.dumps({"success_rate": round(success_rate, 2), "total": len(results)}, indent=4))
