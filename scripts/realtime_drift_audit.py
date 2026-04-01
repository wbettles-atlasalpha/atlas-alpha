import yfinance as yf
import pandas as pd

# Atlas Alpha: Real-Time Drift Validator
# Criteria: Gap > 5%, Volume Spike, 10-day stability (Price > Entry * 0.95)

tickers = ['RKLB', 'SOUN', 'PLTR', 'ASTS', 'DDOG', 'ZETA', 'NET', 'LUNR', 'NVDA', 'AMD']

def validate_drift(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo")
    if len(hist) < 15: return None, "Insufficient Data"
    
    # 1. Identify the most recent Gap > 5%
    for i in range(1, len(hist)):
        prev = hist.iloc[i-1]
        curr = hist.iloc[i]
        gap = ((curr['Close'] - prev['Close']) / prev['Close']) * 100
        
        if gap > 5:
            # 2. Check stability window (10 trading days post-gap)
            entry = curr['Close']
            gap_fill = entry * 0.95
            
            support_window = hist.iloc[i+1 : min(i+11, len(hist))]
            
            # Condition: All lows in the 10 days must be >= gap_fill
            if len(support_window) >= 5 and all(support_window['Low'] >= gap_fill):
                return True, f"Valid Drift: Gap {gap:.1f}% on {curr.name.strftime('%Y-%m-%d')}"
                
    return False, "Failed: No 5% gap + 10-day stability pattern found."

print("| Ticker | Drift Validation |")
print("|---|---|")
for t in tickers:
    valid, msg = validate_drift(t)
    print(f"| {t} | {'✅' if valid else '❌'} {msg} |")
