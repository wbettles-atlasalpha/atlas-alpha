import yfinance as yf
import pandas as pd
import json

# Define representative broad universes (avoiding manual cherry-picking)
# In production, we'd use a full constituent list. Here we scan broader samples.
UNIVERSE = {
    "Nasdaq": ["NVDA", "AMD", "META", "ASML", "ADBE", "SNPS", "CDNS", "PANW", "FTNT", "DDOG", "ZS", "MDB", "CRWD", "NET", "ZETA", "ASTS", "IONQ"],
    "S&P500": ["VRTX", "VRSK", "ANET", "PAYX", "CTSH", "FTV", "MTD", "AMP", "JKHY", "DXCM"],
    "ASX": ["XRO.AX", "PME.AX", "WBT.AX", "NST.AX", "MIN.AX", "TCL.AX", "GMG.AX", "AMC.AX", "STX.AX", "S32.AX"]
}

def scan_anomaly(symbol):
    try:
        df = yf.Ticker(symbol).history(period="2y")
        if len(df) < 200: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        
        vectors = []
        for i in range(200, len(df) - 10):
            # Anomaly Trigger: Volatility Contraction + Volume Drought
            # We are looking for the "Silent" breakout.
            if (df['ATR14'].iloc[i] / df['Close'].iloc[i]) < 0.05:
                # 5-day volume drought (under 80% MA)
                if df['Volume'].iloc[i-5:i].mean() < (0.8 * df['VolMA20'].iloc[i]):
                    # Breakout (over 120% MA)
                    if df['Volume'].iloc[i] > (1.2 * df['VolMA20'].iloc[i]):
                        entry = df['Close'].iloc[i]
                        future = df.iloc[i+1 : i+11]
                        
                        hit_invalidation = False
                        ret = 0
                        for idx, (date, row) in enumerate(future.iterrows()):
                            if row['Low'] < (entry * 0.95): # Invalidation
                                hit_invalidation = True
                                ret = -5.0
                                break
                            ret = ((row['Close'] / entry) - 1) * 100
                        
                        vectors.append({"symbol": symbol, "date": str(df.index[i].date()), "invalidated": hit_invalidation, "return": round(ret, 2)})
        return vectors
    except: return []

audit_log = {}
for universe, tickers in UNIVERSE.items():
    audit_log[universe] = []
    for sym in tickers:
        audit_log[universe].extend(scan_anomaly(sym))

print(json.dumps(audit_log, indent=4))
