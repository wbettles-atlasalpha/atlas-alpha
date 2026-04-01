import yfinance as yf
import pandas as pd
import json

# Universe
SYMBOLS = ['NVDA', 'CRWD', 'DDOG', 'MDB', 'NET']

def run_fundamental_inflection_audit(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # 1. Fundamentals (Quarterly)
        cf = ticker.quarterly_cashflow.T
        if 'Free Cash Flow' not in cf.columns: return []
        
        # 2. Backtest period (2025)
        hist = ticker.history(period="3y")
        
        vectors = []
        # Find quarters with 20% FCF jump
        for i in range(1, len(cf) - 1):
            fcf_curr = cf['Free Cash Flow'].iloc[i]
            fcf_prev = cf['Free Cash Flow'].iloc[i-1]
            
            if fcf_curr > (1.2 * fcf_prev):
                inflection_date = cf.index[i]
                
                # Check for subsequent technical breakout
                window = hist[inflection_date : inflection_date + pd.Timedelta(days=90)]
                if len(window) < 5: continue
                
                vol_ma = window['Volume'].rolling(20).mean()
                
                # Look for volume spike in the quarter following the inflection
                for j in range(len(window)):
                    if window['Volume'].iloc[j] > (1.2 * vol_ma.iloc[j]):
                        entry = window['Close'].iloc[j]
                        ret = ((window['Close'].iloc[-1] / entry) - 1) * 100
                        vectors.append({"symbol": symbol, "return": round(ret, 2)})
                        break
        return vectors
    except: return []

results = []
for s in SYMBOLS:
    results.extend(run_fundamental_inflection_audit(s))

wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
print(json.dumps({"success_rate": round(success_rate, 2), "total": len(results), "sample": results[:10]}, indent=4))
