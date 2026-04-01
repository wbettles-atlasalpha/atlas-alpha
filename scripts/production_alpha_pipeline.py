import yfinance as yf
import requests
import json

API_KEY = "d6n9cvhr01qlnj39nfm0d6n9cvhr01qlnj39nfmg"
UNIVERSE = ['NVDA', 'AMD', 'META', 'AMZN', 'MSFT', 'CRWD', 'DDOG', 'MDB', 'NET']

def get_fundamentals(symbol):
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={API_KEY}"
    resp = requests.get(url).json()
    try:
        metric = resp['metric']
        # Fundamental Scoring (Growth + Margin)
        score = 0
        if metric.get('revenueGrowth5Y', 0) > 20: score += 5
        if metric.get('netMarginAnnual', 0) > 15: score += 5
        return score
    except: return 0

def scan_vcp(symbol):
    df = yf.Ticker(symbol).history(period="1y")
    if len(df) < 50: return 0
    vol_ma = df['Volume'].rolling(20).mean()
    if df['Volume'].iloc[-1] > (1.2 * vol_ma.iloc[-1]): return 5 # Technical score
    return 0

report = []
for sym in UNIVERSE:
    fund_score = get_fundamentals(sym)
    tech_score = scan_vcp(sym)
    if fund_score + tech_score >= 10:
        report.append({"symbol": sym, "score": fund_score + tech_score})

print(json.dumps(report, indent=4))
