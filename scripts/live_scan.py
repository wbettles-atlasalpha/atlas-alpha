import yfinance as yf
import pandas as pd

# Scan for "Earnings Drift" signals to replace existing positions
# Filter: Gap > 5%, Hold 10 days, 20% Allocation (20% of 100k = 20k per trade)
tickers = [
    'ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 
    'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'MQ', 
    'PATH', 'ESTC', 'BILL', 'DT', 'SNOW', 'CRSP', 'EDIT', 'NTLA', 'CRBU'
]

def scan_live():
    candidates = []
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1mo")
            if len(hist) < 15: continue
            
            # Check for most recent "Gap & Hold"
            # Gap > 5% on last day, or held 10 days post-gap
            # Simple check for gap > 5% yesterday
            prev = hist.iloc[-2]
            curr = hist.iloc[-1]
            if ((curr['Close'] - prev['Close']) / prev['Close']) > 0.05:
                # Potential candidate
                candidates.append(symbol)
        except: continue
    return candidates

candidates = scan_live()
print(f"Candidates: {candidates}")
