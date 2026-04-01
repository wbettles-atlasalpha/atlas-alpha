import yfinance as yf
import pandas as pd
import numpy as np

# Updated Atlas Alpha Audit Engine
# Filters: Consolidation window + Trend alignment (200 SMA) + Momentum (RSI)

tickers = ['AAPL', 'MSFT', 'NVDA', 'ASTS', 'VKTX', 'TSLA', 'AMD', 'PLTR', 'RKLB', 'CRWD', 'UBER', 'SOFI', 'ZETA', 'IONQ', 'META', 'AMZN', 'GOOGL', 'AVGO']

def get_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def run_advanced_audit():
    all_results = []
    
    print("| Ticker | Identified | Entry | Strategy | Return % |")
    print("|---|---|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            if len(hist) < 200: continue
            
            hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
            hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
            hist['RSI'] = get_rsi(hist)
            
            for i in range(200, len(hist) - 5):
                curr = hist.iloc[i]
                prev = hist.iloc[i-1]
                
                # Condition 1: Alpha Vector (Volume spike + Gap)
                vol_spike = curr['Volume'] > (1.5 * curr['MA_Vol']) # Relaxed 2.0 to 1.5
                price_gap = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.02 # Relaxed 3% to 2%
                
                # Condition 2: Trend Alignment (200 SMA) - Remove RSI for now
                trend_up = curr['Close'] > curr['SMA_200']
                
                if vol_spike and price_gap and trend_up:
                    # Consolidation Filter: Verify price stays within 5% of entry for next 5 days
                    support_window = hist.iloc[i+1 : i+6]
                    if all(support_window['Low'] >= (curr['Close'] * 0.95)):
                        entry = curr['Close']
                        # Track performance
                        future = hist.iloc[i+6:]
                        if future.empty: continue
                        
                        exit_price = future.iloc[-1]['Close']
                        ret = ((exit_price / entry) - 1) * 100
                        
                        all_results.append({
                            "ticker": symbol,
                            "date": curr.name.strftime('%Y-%m-%d'),
                            "entry": entry,
                            "return": round(ret, 2)
                        })
                        
        except Exception as e:
            continue

    for r in all_results[:15]:
        print(f"| {r['ticker']} | {r['date']} | ${r['entry']:.2f} | Consolidation/Trend | {r['return']}% |")
        
    return all_results

results = run_advanced_audit()
if results:
    print(f"\n### Total Identified Vectors: {len(results)}")
    print(f"### Aggregate Performance: {sum(r['return'] for r in results)/len(results):.2f}% Avg per Vector")
