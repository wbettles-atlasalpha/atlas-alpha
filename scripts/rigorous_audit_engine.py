import yfinance as yf
import pandas as pd
import json

# Comprehensive lists for Audit (Partial representative sets due to API limits)
NASDAQ_TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "META", "GOOGL", "AVGO", "TSLA", "COST", "PEP", "ADBE", "AMD", "NFLX", "INTC", "CSCO", "CMCSA", "AMGN", "HON", "TXN", "QCOM", "TMUS", "INTU", "SBUX", "GILD", "MDLZ", "BKNG", "ADP", "VRTX", "MU", "REGN"]
ASX_TICKERS = ["BHP.AX", "CBA.AX", "CSL.AX", "NAB.AX", "WBC.AX", "ANZ.AX", "WDS.AX", "RIO.AX", "MQG.AX", "WOW.AX", "WES.AX", "TLS.AX", "FMG.AX", "COL.AX", "TCL.AX", "GMG.AX", "AMC.AX", "STX.AX", "XRO.AX", "SUN.AX"]

def run_rigorous_audit(index_name, tickers):
    vectors = []
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start="2025-01-01", end="2025-12-31")
            if len(hist) < 20: continue
            
            for i in range(1, len(hist) - 10):
                prev = hist.iloc[i-1]
                curr = hist.iloc[i]
                
                # Gap Up > 5%
                if ((curr['Close'] - prev['Close']) / prev['Close']) > 0.05:
                    entry = curr['Close']
                    stop_loss = entry * 0.95
                    
                    # Look ahead 5 days for profit, or until invalidation
                    future = hist.iloc[i+1 : i+6]
                    
                    hit_invalidation = False
                    final_return = 0
                    days_held = 0
                    
                    for idx, (date, row) in enumerate(future.iterrows()):
                        days_held = idx + 1
                        if row['Low'] < stop_loss:
                            hit_invalidation = True
                            final_return = -5.0 # Stop loss hit
                            break
                        final_return = ((row['Close'] / entry) - 1) * 100
                    
                    vectors.append({
                        "symbol": symbol,
                        "date": str(curr.name.date()),
                        "entry": round(entry, 2),
                        "invalidated": hit_invalidation,
                        "days_held": days_held,
                        "return": round(final_return, 2)
                    })
        except:
            continue
    return vectors

if __name__ == "__main__":
    report = {
        "Nasdaq 100": run_rigorous_audit("Nasdaq 100", NASDAQ_TICKERS),
        "ASX 200": run_rigorous_audit("ASX 200", ASX_TICKERS)
    }
    print(json.dumps(report, indent=4))
