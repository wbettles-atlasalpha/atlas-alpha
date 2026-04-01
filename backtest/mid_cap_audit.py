import yfinance as yf
import pandas as pd

# Mid-cap growth strategy (The "Unknown Mover" Scan)
# Target: Mid-cap growth, 1.2x Vol Spike, No strict SMA 200, Simple momentum
tickers = [
    'ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 
    'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'MQ', 
    'PATH', 'ESTC', 'BILL', 'DT', 'SNOW', 'CRSP', 'EDIT', 'NTLA', 'CRBU'
]

def run_mid_cap_audit():
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
                
                # Loose scan to find ANY high-growth movement
                if curr['Volume'] > (1.2 * curr['MA_Vol']) and ((curr['Close'] - prev['Close']) / prev['Close']) > 0.015:
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
            
    print(f"\n### Total Mid-Cap Vectors Identified: {len(results)}")
    if results:
        print(f"### Avg Return per Vector: {sum(results)/len(results):.2f}%")

run_mid_cap_audit()
