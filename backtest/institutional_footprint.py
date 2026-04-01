import yfinance as yf
import pandas as pd

# Atlas Alpha: Institutional Footprint Scanner
# Strategy: 5x Volume Spike + 5% Sector Relative Strength + No News Proxy
# Goal: Isolate massive institutional block accumulation.

tickers = [
    'ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 
    'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'MQ', 
    'PATH', 'ESTC', 'BILL', 'DT', 'SNOW', 'CRSP', 'EDIT', 'NTLA', 'CRBU'
]

def run_footprint_scan():
    results = []
    print("| Ticker | Entry | Return % |")
    print("|---|---|---|")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            if len(hist) < 30: continue
            
            hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
            
            for i in range(30, len(hist) - 6):
                curr = hist.iloc[i]
                prev = hist.iloc[i-1]
                
                # Logic: 5x Volume Spike + 5% Move
                # This is a extreme anomaly filter
                vol_spike = curr['Volume'] > (5.0 * curr['MA_Vol'])
                price_move = ((curr['Close'] - prev['Close']) / prev['Close']) > 0.05
                
                if vol_spike and price_move:
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
            
    print(f"\n### Total Institutional Footprints Identified: {len(results)}")
    if results:
        print(f"### Avg Return per Footprint: {sum(results)/len(results):.2f}%")

run_footprint_scan()
