import yfinance as yf
import pandas as pd
import json

SYMBOLS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET']

def run_high_conviction_audit(symbol):
    try:
        df = yf.Ticker(symbol).history(period="2y")
        if len(df) < 300: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        df['52w_High'] = df['Close'].rolling(252).max()
        
        vectors = []
        for i in range(200, len(df) - 10):
            # 1. Trend Gate: Price > 50 & 200 SMA
            if df['Close'].iloc[i] < df['SMA50'].iloc[i] or df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. Relative Strength Gate: Price > 80% of 52w High
            if df['Close'].iloc[i] < (df['52w_High'].iloc[i] * 0.8): continue
            
            # 3. Institutional Footprint: Volume > 150% MA (High conviction)
            if df['Volume'].iloc[i] > (1.5 * df['VolMA20'].iloc[i]):
                # Vector Logic: Check for Profit after 10 days
                ret = ((df['Close'].iloc[i+10] / df['Close'].iloc[i]) - 1) * 100
                vectors.append({"symbol": symbol, "return": round(ret, 2)})
        return vectors
    except: return []

results = []
for s in SYMBOLS:
    results.extend(run_high_conviction_audit(s))

wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
print(json.dumps({"success_rate": round(success_rate, 2), "total": len(results)}, indent=4))
