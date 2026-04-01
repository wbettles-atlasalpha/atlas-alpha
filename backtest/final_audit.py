import yfinance as yf
import pandas as pd
import numpy as np

tickers = [
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AVGO', 'AMD', 'PLTR', 'RKLB', 'CRWD', 'UBER', 'SOFI', 'ZETA', 'IONQ',
    'GS', 'JPM', 'CAT', 'HON', 'BA', 'MCD', 'DIS', 'CVX', 'XOM', 'PG', 'KO', 'JNJ'
]

def run_relaxed_audit():
    results = []
    print("| Ticker | Entry | Return % |")
    print("|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            if len(hist) < 200: continue
            
            hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
            hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
            
            for i in range(200, len(hist) - 6):
                curr = hist.iloc[i]
                prev = hist.iloc[i-1]
                
                # Logic: Relaxed Gap (1.5%) and Volume (1.3x)
                vol_spike = curr['Volume'] > (1.3 * curr['MA_Vol'])
                price_gap = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.015
                trend_up = curr['Close'] > curr['SMA_200']
                
                if vol_spike and price_gap and trend_up:
                    # Relaxed Consolidation Filter: Close must remain above entry - 3%
                    support_window = hist.iloc[i+1 : i+6]
                    if all(support_window['Close'] >= (curr['Close'] * 0.97)):
                        entry = curr['Close']
                        exit_price = hist.iloc[i+6]['Close']
                        ret = ((exit_price / entry) - 1) * 100
                        results.append(ret)
                        if len(results) <= 15:
                            print(f"| {symbol} | ${entry:.2f} | {ret:.2f}% |")

        except Exception as e:
            continue
            
    print(f"\n### Total Vectors Identified (Relaxed): {len(results)}")
    if results:
        print(f"### Avg Return per Vector: {sum(results)/len(results):.2f}%")

run_relaxed_audit()
