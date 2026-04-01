import yfinance as yf
import pandas as pd
import numpy as np

# Comprehensive scan of high-growth tech and index proxies
tickers = [
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AVGO', 'COST', 'PEP', 'ADBE', 'NFLX', 'AMD', 'QCOM', 'INTC', 
    'AMAT', 'TXN', 'GILD', 'INTU', 'FISV', 'BKNG', 'ADP', 'CSX', 'MU', 'LRCX', 'AMGN', 'ISRG', 'MDLZ', 'ADI', 'VRTX',
    'ASTS', 'VKTX', 'PLTR', 'RKLB', 'CRWD', 'UBER', 'SOFI', 'ZETA', 'IONQ', 'SHOP', 'DDOG', 'SNOW', 'MDB', 'NET', 'DDOG',
    'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'PTON', 'TDOC'
]

def run_comprehensive_audit():
    results = []
    
    print("| Ticker | Entry | Return % |")
    print("|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            if len(hist) < 30: continue
            
            hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
            
            # Identify all signals without the consolidation filter
            for i in range(30, len(hist) - 1):
                curr = hist.iloc[i]
                prev = hist.iloc[i-1]
                
                vol_spike = curr['Volume'] > (1.5 * curr['MA_Vol'])
                price_gap = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.02
                
                if vol_spike and price_gap:
                    entry = curr['Close']
                    invalidation = entry * 0.95
                    
                    # Track performance: Hit -5% or end of data
                    ret = 0.0
                    for j in range(i + 1, len(hist)):
                        future = hist.iloc[j]
                        if future['Low'] <= invalidation:
                            ret = -5.0
                            break
                        # Check exit on potential move after 5 days
                        if j == i + 5:
                            ret = ((future['Close'] / entry) - 1) * 100
                            break
                    
                    results.append(ret)
                    if len(results) <= 15:
                        print(f"| {symbol} | ${entry:.2f} | {ret:.2f}% |")

        except Exception as e:
            continue
            
    print(f"\n### Total Vectors Identified: {len(results)}")
    print(f"### Average Return: {sum(results)/len(results):.2f}%")

run_comprehensive_audit()
