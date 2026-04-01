import yfinance as yf
import pandas as pd

# Broader Market Drift Scan
# We scan S&P 500 (SPY components) and Nasdaq 100 (QQQ components)
# to find "Earnings Drift" signals (Gap > 5% + Stability)

# Get full constituents (simplified for script efficiency)
# Using a representative list of tech/high-growth from SPY/QQQ
tickers = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'AVGO', 'PEP', 'COST', 
    'ADBE', 'AMD', 'NFLX', 'CSCO', 'INTC', 'CMCSA', 'INTU', 'AMGN', 'BKNG', 'HON',
    'QCOM', 'TXN', 'SBUX', 'AMAT', 'MDLZ', 'GILD', 'ISRG', 'BKNG', 'ADP', 'MU',
    'PANW', 'SNOW', 'DDOG', 'CRWD', 'ZS', 'PLTR', 'RKLB', 'ASTS', 'SOUN', 'ZETA'
]

def scan_broad_market():
    candidates = []
    print(f"Scanning {len(tickers)} tickers for Atlas Alpha Drift signals...")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="3mo")
            if len(hist) < 20: continue
            
            # Look for Gap Up > 5% within the last 15 days
            for i in range(1, len(hist) - 5):
                prev = hist.iloc[i-1]
                curr = hist.iloc[i]
                
                if ((curr['Close'] - prev['Close']) / prev['Close']) > 0.05:
                    entry = curr['Close']
                    gap_fill = entry * 0.95
                    
                    # Check if it has held the gap-fill level for at least 5 days
                    # and price is still near entry (drift)
                    support_window = hist.iloc[i+1 : min(i+6, len(hist))]
                    
                    if len(support_window) >= 5 and all(support_window['Low'] >= gap_fill):
                        # Signal found
                        candidates.append({
                            "symbol": symbol,
                            "entry": entry,
                            "current": hist.iloc[-1]['Close']
                        })
                        break # Found a valid setup for this ticker
        except: continue
        
    return candidates

signals = scan_broad_market()
print(f"Found {len(signals)} potential candidates:")
for s in signals:
    print(f"Signal: {s['symbol']} | Entry: ${s['entry']:.2f} | Current: ${s['current']:.2f}")
