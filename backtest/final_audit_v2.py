import yfinance as yf

# Simplified Audit Engine: Just find the Alpha Vectors
# No complex filters to ensure we actually see the market first.

tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AMD', 'PLTR', 'RKLB', 'CRWD']

def run_simple_scan():
    results = []
    print("| Ticker | Entry | Return % |")
    print("|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            if len(hist) < 30: continue
            
            hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
            
            # Simple condition: 1.5x Vol + 2% Gap
            for i in range(30, len(hist) - 1):
                curr = hist.iloc[i]
                prev = hist.iloc[i-1]
                
                if curr['Volume'] > (1.5 * curr['MA_Vol']) and ((curr['Close'] - prev['Close']) / prev['Close']) > 0.02:
                    entry = curr['Close']
                    future = hist.iloc[i+1:]
                    if not future.empty:
                        # Exit: next 5-day return
                        exit_price = future.iloc[min(5, len(future)-1)]['Close']
                        ret = ((exit_price / entry) - 1) * 100
                        results.append(ret)
                        if len(results) <= 15:
                            print(f"| {symbol} | ${entry:.2f} | {ret:.2f}% |")

        except Exception as e:
            continue
            
    print(f"\n### Total Vectors Identified: {len(results)}")
    if results:
        print(f"### Aggregate Return: {sum(results)/len(results):.2f}%")

run_simple_scan()
