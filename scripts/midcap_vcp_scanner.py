import yfinance as yf
import json

# Broad list of Mid/Small Cap growth candidates (avoiding blue-chip index components)
# We add a market cap filter to this list to ensure no big names sneak in.
CANDIDATES = [
    'ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 
    'ESTC', 'BILL', 'DT', 'SNOW', 'CRSP', 'EDIT', 'NTLA', 'CRBU', 'MQG.AX', 'XRO.AX',
    'PME.AX', 'WBT.AX', 'STX.AX', 'PLS.AX', 'VUL.AX', 'IMU.AX', 'LKE.AX', 'CXO.AX'
]

def scan_midcap_vcp(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        # Strict Market Cap Filter
        if info.get('marketCap', 0) > 10000000000: return None
        
        df = ticker.history(period="1y")
        if len(df) < 200: return None
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        
        vectors = []
        for i in range(200, len(df) - 10):
            # Strict VCP: ATR < 5% of price, Vol Drought < 80% of MA, Breakout > 120%
            if (df['ATR14'].iloc[i] / df['Close'].iloc[i]) < 0.05:
                if df['Volume'].iloc[i-5:i].mean() < (0.8 * df['VolMA20'].iloc[i]):
                    if df['Volume'].iloc[i] > (1.2 * df['VolMA20'].iloc[i]):
                        vectors.append({
                            "symbol": symbol,
                            "date": str(df.index[i].date()),
                            "entry": round(df['Close'].iloc[i], 2),
                            "return": round(((df['Close'].iloc[i+10] / df['Close'].iloc[i]) - 1) * 100, 2)
                        })
        return vectors
    except: return None

audit = {}
for sym in CANDIDATES:
    res = scan_midcap_vcp(sym)
    if res: audit[sym] = res

print(json.dumps(audit, indent=4))
