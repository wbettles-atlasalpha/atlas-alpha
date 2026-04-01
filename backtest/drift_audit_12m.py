import yfinance as yf
import pandas as pd

# Atlas Alpha: 12-Month Institutional Drift Audit
# Comprehensive scan: S&P 500, Nasdaq, Dow, and ASX components.

tickers = [
    # US Tech/Growth (Nasdaq/S&P)
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AVGO', 'AMD', 'PLTR', 
    # US Industrials (Dow)
    'GS', 'JPM', 'CAT', 'HON', 'BA', 'MCD', 'DIS', 'CVX', 'XOM',
    # ASX (Australia)
    'BHP.AX', 'CBA.AX', 'CSL.AX', 'NAB.AX', 'WBC.AX', 'ANZ.AX', 'MQG.AX', 'RIO.AX'
]

def run_12m_audit():
    results = []
    print(f"| Ticker | Entry | Return % |")
    print(f"|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            # 12 months of data
            hist = ticker.history(period="1y")
            if len(hist) < 20: continue
            
            for i in range(1, len(hist) - 15):
                prev = hist.iloc[i-1]
                curr = hist.iloc[i]
                
                # Gap Up > 5%
                gap_up = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.05
                
                if gap_up:
                    entry = curr['Close']
                    gap_fill = entry * 0.95
                    
                    # Consolidation: Check if price holds the 5% gap-fill level for next 10 days
                    support_window = hist.iloc[i+1 : i+11]
                    if len(support_window) == 10 and all(support_window['Low'] >= gap_fill):
                        # Exit: 5-day return after 10-day hold
                        future = hist.iloc[i+11:]
                        if not future.empty:
                            exit_price = future.iloc[min(5, len(future)-1)]['Close']
                            ret = ((exit_price / entry) - 1) * 100
                            results.append(ret)
                            if len(results) <= 15:
                                print(f"| {symbol} | ${entry:.2f} | {ret:.2f}% |")

        except Exception as e:
            continue
            
    print(f"\n### Total Vectors Identified (12M): {len(results)}")
    if results:
        print(f"### Avg Return per Vector: {sum(results)/len(results):.2f}%")

run_12m_audit()
