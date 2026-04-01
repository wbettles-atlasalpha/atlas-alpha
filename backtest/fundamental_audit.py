import yfinance as yf
import pandas as pd
import numpy as np

# Atlas Alpha: Enhanced Mid-Cap Growth Strategy
# Strategy: 
# 1. Volume Decay (20-day decreasing trend) before Spike
# 2. Higher Low (Price > 20-day low)
# 3. Fundamental Filter (EPS Growth > 10% or P/E < 50)

tickers = [
    'ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 
    'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'MQ', 
    'PATH', 'ESTC', 'BILL', 'DT', 'SNOW', 'CRSP', 'EDIT', 'NTLA', 'CRBU'
]

def run_fundamental_audit():
    results = []
    print("| Ticker | Entry | Return % |")
    print("|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="6mo")
            if len(hist) < 40: continue
            
            # Fundamental Filter: 
            # Require EPS growth or reasonable P/E to ensure growth validity
            eps_growth = info.get('earningsGrowth', 0)
            pe_ratio = info.get('trailingPE', 100)
            
            # Filter: If EPS growth < 0 and PE > 50, skip (avoid garbage)
            if (eps_growth is None or eps_growth < 0.1) and pe_ratio > 50:
                continue

            hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
            
            for i in range(30, len(hist) - 6):
                curr = hist.iloc[i]
                prev = hist.iloc[i-1]
                window = hist.iloc[i-20:i]
                
                # Filter 1: Volume Decay (Last 5 days volume < 30-day average)
                vol_decay = all(window['Volume'].tail(5) < window['MA_Vol'].tail(5))
                
                # Filter 2: Higher Low (Price > 20-day Low)
                higher_low = curr['Low'] > window['Low'].min()
                
                # Filter 3: Alpha Vector (1.3x Vol spike + 2% Gap)
                vol_spike = curr['Volume'] > (1.3 * curr['MA_Vol'])
                price_gap = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.02
                
                if vol_decay and higher_low and vol_spike and price_gap:
                    entry = curr['Close']
                    future = hist.iloc[i+1:i+6]
                    if not future.empty:
                        exit_price = future.iloc[-1]['Close']
                        ret = ((exit_price / entry) - 1) * 100
                        results.append(ret)
                        if len(results) <= 15:
                            print(f"| {symbol} | ${entry:.2f} | {ret:.2f}% |")

        except Exception as e:
            continue
            
    print(f"\n### Total High-Conviction Vectors: {len(results)}")
    if results:
        print(f"### Avg Return per Vector: {sum(results)/len(results):.2f}%")

run_fundamental_audit()
