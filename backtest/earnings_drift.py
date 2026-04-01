import yfinance as yf
import pandas as pd

# Atlas Alpha: Earnings Drift Strategy
# Strategy: Gap Up > 5% on Earnings/Catalyst, hold gap-fill level (Entry - 5%) for 10 trading days.
# Goal: Isolate institutional accumulation post-catalyst.

tickers = [
    'ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 
    'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'MQ', 
    'PATH', 'ESTC', 'BILL', 'DT', 'SNOW', 'CRSP', 'EDIT', 'NTLA', 'CRBU'
]

def run_drift_scan():
    results = []
    print("| Ticker | Entry | Return % |")
    print("|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            if len(hist) < 20: continue
            
            for i in range(1, len(hist) - 10):
                prev = hist.iloc[i-1]
                curr = hist.iloc[i]
                
                # Gap Up > 5%
                gap_up = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.05
                
                if gap_up:
                    entry = curr['Close']
                    gap_fill = entry * 0.95 # Threshold
                    
                    # Consolidate: Check if price holds the 5% gap-fill level for next 10 days
                    support_window = hist.iloc[i+1 : i+11]
                    if len(support_window) == 10 and all(support_window['Low'] >= gap_fill):
                        # Successful accumulation pattern found
                        future = hist.iloc[i+11:]
                        if not future.empty:
                            exit_price = future.iloc[min(5, len(future)-1)]['Close']
                            ret = ((exit_price / entry) - 1) * 100
                            results.append(ret)
                            if len(results) <= 15:
                                print(f"| {symbol} | ${entry:.2f} | {ret:.2f}% |")

        except Exception as e:
            continue
            
    print(f"\n### Total Earnings Drift Vectors Identified: {len(results)}")
    if results:
        print(f"### Avg Return per Drift Vector: {sum(results)/len(results):.2f}%")

run_drift_scan()
