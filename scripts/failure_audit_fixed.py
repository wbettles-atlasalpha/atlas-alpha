import yfinance as yf
import pandas as pd
import json

# Load the current results (from previous precision scan)
with open('/home/warwick/.openclaw/workspace/precision_audit_results.json', 'r') as f:
    results = json.load(f)

def audit_failures():
    failure_data = []
    
    for symbol, vectors in results.items():
        # Get historical data for the ticker
        df = yf.Ticker(symbol).history(period="2y")
        # Ensure index is tz-naive
        df.index = df.index.tz_localize(None)
        
        # Calculate Technicals for the whole dataframe
        df['SMA50'] = df['Close'].rolling(50).mean()
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = delta.clip(upper=0).abs()
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Analyze failures
        for v in vectors:
            if v['invalidated']:
                date = pd.to_datetime(v['date'])
                
                # Get state at failure date
                if date in df.index:
                    state = df.loc[date]
                    dist_sma50 = (state['Close'] / state['SMA50']) - 1
                    
                    failure_data.append({
                        "symbol": symbol,
                        "date": v['date'],
                        "rsi": round(state['RSI'], 2),
                        "dist_sma50": round(dist_sma50, 4)
                    })
    return failure_data

print(json.dumps(audit_failures(), indent=4))
