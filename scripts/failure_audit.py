import yfinance as yf
import pandas as pd
import json

# Load the current results
with open('/home/warwick/.openclaw/workspace/precision_audit_results.json', 'r') as f:
    results = json.load(f)

def audit_failures():
    failure_data = []
    
    for symbol, vectors in results.items():
        # Get historical data for the ticker
        df = yf.Ticker(symbol).history(period="2y")
        
        # Analyze failures
        for v in vectors:
            if v['invalidated']:
                date = pd.to_datetime(v['date'])
                
                # Fetch state at failure time
                state = df.loc[:date].iloc[-1]
                
                # Calculate indicators at the time of failure
                rsi = 100 - (100 / (1 + (df['Close'].diff().clip(lower=0).rolling(14).mean() / df['Close'].diff().clip(upper=0).abs().rolling(14).mean())))
                dist_sma50 = (df['Close'].iloc[-1] / df['Close'].rolling(50).mean().iloc[-1]) - 1
                
                failure_data.append({
                    "symbol": symbol,
                    "date": v['date'],
                    "rsi": round(rsi.iloc[-1], 2),
                    "dist_sma50": round(dist_sma50, 4)
                })
    return failure_data

print(json.dumps(audit_failures(), indent=4))
