import yfinance as yf
import pandas as pd

# The Atlas Alpha Audit Engine
# Scans a list of high-growth tickers (S&P 500/Nasdaq proxy)
# Identifies Alpha Vectors, tracks performance, exits at -5% invalidation.

tickers = ['AAPL', 'MSFT', 'NVDA', 'ASTS', 'VKTX', 'TSLA', 'AMD', 'PLTR', 'RKLB', 'CRWD', 'UBER', 'SOFI', 'ZETA', 'IONQ', 'META', 'AMZN', 'GOOGL', 'AVGO']

def run_audit():
    all_results = []
    
    print("| Ticker | Identified | Entry | Invalidation | Exit | Return % |")
    print("|---|---|---|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
            
            for i in range(30, len(hist)):
                curr = hist.iloc[i]
                prev = hist.iloc[i-1]
                
                vol_spike = curr['Volume'] > (2 * curr['MA_Vol'])
                price_gap = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.03
                
                if vol_spike and price_gap:
                    entry = curr['Close']
                    invalidation = entry * 0.95
                    
                    # Track performance until invalidation or end of period
                    trade_closed = False
                    for j in range(i + 1, len(hist)):
                        future = hist.iloc[j]
                        if future['Low'] <= invalidation:
                            ret = -5.0
                            exit_price = invalidation
                            trade_closed = True
                            break
                    
                    if not trade_closed:
                        exit_price = hist.iloc[-1]['Close']
                        ret = ((exit_price / entry) - 1) * 100
                    
                    all_results.append({
                        "ticker": symbol,
                        "date": curr.name.strftime('%Y-%m-%d'),
                        "entry": entry,
                        "invalidation": invalidation,
                        "exit": exit_price,
                        "return": round(ret, 2)
                    })
                    
        except Exception as e:
            continue

    # Report results
    for r in all_results[:15]: # Show top 15 samples
        print(f"| {r['ticker']} | {r['date']} | ${r['entry']:.2f} | ${r['invalidation']:.2f} | ${r['exit']:.2f} | {r['return']}% |")
        
    return all_results

results = run_audit()
total_ret = sum(r['return'] for r in results)
print(f"\n### Total Identified Vectors: {len(results)}")
print(f"### Aggregate Performance: {sum(r['return'] for r in results)/len(results):.2f}% Avg per Vector")
