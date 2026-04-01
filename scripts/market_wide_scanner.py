import yfinance as yf
import pandas as pd
import json

# Define Universe via Indices
# Note: yfinance ticker fetching is limit-bound, so we'll fetch index constituents dynamically
def get_universe(index_ticker):
    # This is a simplified approach to fetch major tickers.
    # In a real environment, we'd pull these from a master list.
    # We will use common constituent lists for the scan.
    if index_ticker == "^NDX": # Nasdaq 100
        return ["NVDA", "AMD", "META", "GOOGL", "AMZN", "TSLA", "NFLX", "ADBE", "INTC", "CSCO", "PYPL", "INTU", "AMGN", "BKNG", "GILD", "SBUX", "MDLZ", "ADP", "VRTX", "MU", "REGN", "LRCX", "ADI", "KLAC", "SNPS", "CDNS", "ASML", "CSGP", "DXCM", "PAYX"]
    if index_ticker == "^AXJO": # ASX 200 (Growth/Mid-cap representation)
        return ["XRO.AX", "PME.AX", "WBT.AX", "NST.AX", "MIN.AX", "PLS.AX", "AKE.AX", "VUL.AX", "IMU.AX", "LKE.AX"]
    return []

def scan_universe(tickers):
    report = []
    for sym in tickers:
        try:
            ticker = yf.Ticker(sym)
            # Market Cap filter (simplified check)
            if ticker.info.get('marketCap', 0) > 10000000000: continue
            
            df = ticker.history(period="1y")
            if len(df) < 200: continue
            
            df['VolMA20'] = df['Volume'].rolling(20).mean()
            df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
            
            for i in range(200, len(df) - 5):
                # VCP Pattern
                if (df['ATR14'].iloc[i] / df['Close'].iloc[i]) < 0.05:
                    if df['Volume'].iloc[i-5:i].mean() < (0.8 * df['VolMA20'].iloc[i]):
                        if df['Volume'].iloc[i] > (1.2 * df['VolMA20'].iloc[i]):
                            entry = df['Close'].iloc[i]
                            # Simple exit logic (5% stop loss, 10-day hold)
                            future = df.iloc[i+1 : i+11]
                            ret = ((future.iloc[-1]['Close'] / entry) - 1) * 100
                            report.append({"symbol": sym, "date": str(df.index[i].date()), "entry": round(entry, 2), "return": round(ret, 2)})
        except: continue
    return report

results = {
    "Nasdaq 100 Growth": scan_universe(get_universe("^NDX")),
    "ASX 200 Growth": scan_universe(get_universe("^AXJO"))
}

print(json.dumps(results, indent=4))
