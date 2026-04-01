import requests
import yfinance as yf
import pandas as pd
import json

# Using the Finnhub API Key from TOOLS.md
API_KEY = "d6n9cvhr01qlnj39nfm0d6n9cvhr01qlnj39nfmg"
SYMBOLS = ['NVDA', 'CRWD', 'DDOG', 'MDB', 'NET']

def get_fcf_history(symbol):
    url = f"https://finnhub.io/api/v1/stock/financials-reported?symbol={symbol}&token={API_KEY}"
    resp = requests.get(url).json()
    
    # Extract FCF from Finnhub "reported" financials
    # This is complex, so we simplify: look for "NetCashFlow" in the reported data
    if 'data' not in resp: return None
    
    fcf_history = []
    for report in resp['data']:
        # Finnhub reported financials are a deep JSON structure
        # Looking for FCF/Cash Flow from Operating Activities
        for item in report['report']['cash']:
            if item['concept'] == 'us-gaap_NetCashFlowsFromUsedInOperatingActivities':
                fcf_history.append({"date": report['filedDate'], "fcf": item['value']})
    return fcf_history

def run_precision_audit(symbol):
    fcf_data = get_fcf_history(symbol)
    if not fcf_data or len(fcf_data) < 4: return []
    
    # Convert to DF
    df_fcf = pd.DataFrame(fcf_data)
    df_fcf['date'] = pd.to_datetime(df_fcf['date'])
    df_fcf = df_fcf.sort_values('date')
    
    # Get Technicals
    hist = yf.Ticker(symbol).history(start="2024-01-01", end="2025-12-31")
    
    vectors = []
    for i in range(1, len(df_fcf)):
        # Inflection: FCF Jump > 20%
        if df_fcf['fcf'].iloc[i] > (1.2 * df_fcf['fcf'].iloc[i-1]):
            inflection_date = df_fcf['date'].iloc[i]
            
            # Technical Breakout Check (in the 60 days post-inflection)
            window = hist[inflection_date : inflection_date + pd.Timedelta(days=60)]
            if len(window) < 5: continue
            
            vol_ma = window['Volume'].rolling(20).mean()
            for idx, (date, row) in enumerate(window.iterrows()):
                if row['Volume'] > (1.5 * vol_ma.iloc[idx]):
                    ret = ((window['Close'].iloc[-1] / row['Close']) - 1) * 100
                    vectors.append({"symbol": symbol, "inflection": str(inflection_date.date()), "return": round(ret, 2)})
                    break
    return vectors

final_results = []
for s in SYMBOLS:
    final_results.extend(run_precision_audit(s))

print(json.dumps(final_results, indent=4))
