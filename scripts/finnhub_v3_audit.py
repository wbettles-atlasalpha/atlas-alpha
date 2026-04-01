import requests
import yfinance as yf
import pandas as pd
import json

# API Key
API_KEY = "d6n9cvhr01qlnj39nfm0d6n9cvhr01qlnj39nfmg"
SYMBOLS = ['NVDA', 'CRWD', 'DDOG', 'MDB', 'NET']

def get_fcf(symbol):
    # Finnhub simplified financials
    url = f"https://finnhub.io/api/v1/stock/financials?symbol={symbol}&metric=all&token={API_KEY}"
    resp = requests.get(url).json()
    try:
        # FCF is often reported as 'freeCashFlow' in the 'series' metric
        fcf_series = resp['series']['annual']['freeCashFlow']
        return fcf_series # Returns list of {period, v}
    except: return []

def audit_v3(symbol):
    fcf = get_fcf(symbol)
    if not fcf: return []
    
    df = yf.Ticker(symbol).history(period="2y")
    
    vectors = []
    # Find FCF jumps in historical data
    for i in range(1, len(fcf)):
        if fcf[i]['v'] > (1.2 * fcf[i-1]['v']): # 20% FCF Jump
            inflection = pd.to_datetime(fcf[i]['period'])
            # Check price breakout post inflection
            window = df[inflection : inflection + pd.Timedelta(days=90)]
            if len(window) < 5: continue
            
            vol_ma = window['Volume'].rolling(20).mean()
            # Technical Breakout
            for idx, (date, row) in enumerate(window.iterrows()):
                if row['Volume'] > (1.2 * vol_ma.iloc[idx]):
                    ret = ((window['Close'].iloc[-1] / row['Close']) - 1) * 100
                    vectors.append({"symbol": symbol, "return": round(ret, 2)})
                    break
    return vectors

final = []
for s in SYMBOLS:
    final.extend(audit_v3(s))

print(json.dumps(final, indent=4))
