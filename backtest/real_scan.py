import yfinance as yf
import pandas as pd

# This script performs a REAL backtest on a specific ticker (ASTS) 
# using yfinance data to identify genuine "Alpha Vector" triggers 
# over the last 180 days.

def analyze_ticker(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="6mo")
    
    # Calculate 30-day Moving Avg Volume
    hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
    
    # Detect Alpha Vectors
    # Condition: Volume > 200% MA AND Price Gap > 3%
    vectors = []
    
    for i in range(30, len(hist)):
        curr = hist.iloc[i]
        prev = hist.iloc[i-1]
        
        vol_spike = curr['Volume'] > (2 * curr['MA_Vol'])
        price_gap = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.03
        
        if vol_spike and price_gap:
            vectors.append({
                "Date": curr.name.strftime('%Y-%m-%d'),
                "Entry": curr['Close'],
                "Invalidation": curr['Close'] * 0.95
            })
            
    return vectors

print(f"| Date | Entry Price | Invalidation |")
print(f"|---|---|---|")
for v in analyze_ticker("ASTS"):
    print(f"| {v['Date']} | ${v['Entry']:.2f} | ${v['Invalidation']:.2f} |")
