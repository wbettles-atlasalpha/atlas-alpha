import os
import json
import urllib.request
import datetime

FINNHUB_KEY = os.environ.get("FINNHUB_API_KEY", "d6n9cvhr01qlnj39nfm0d6n9cvhr01qlnj39nfmg")

WATCHLIST = {
    "Quantum & Photonics": ["IONQ", "RGTI", "QBTS", "LITE"],
    "Next-Gen Defense & Space": ["LUNR", "ASTS", "KTOS", "AVAV", "SPIR"],
    "AI Infra (Power & Cooling)": ["MOD", "NVT", "POWL", "HWM"],
    "Biotech & Genomics": ["CRSP", "NTLA", "VKTX", "RXRX"]
}

def fetch_data(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return None

def main():
    print("==================================================================")
    print("             ATLAS ALPHA: SHADOW MOONSHOT SCANNER                 ")
    print("==================================================================")
    
    today = datetime.datetime.now()
    six_months_ago = (today - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')

    for sector, tickers in WATCHLIST.items():
        print(f"\n[{sector.upper()}]")
        for sym in tickers:
            # Get basic metrics (Volume anomalies)
            metric_url = f"https://finnhub.io/api/v1/stock/metric?symbol={sym}&metric=all&token={FINNHUB_KEY}"
            metrics = fetch_data(metric_url)
            
            # Get Insider Sentiment
            insider_url = f"https://finnhub.io/api/v1/stock/insider-sentiment?symbol={sym}&from={six_months_ago}&to={today_str}&token={FINNHUB_KEY}"
            insider_data = fetch_data(insider_url)

            # Parse metrics
            vol_10d = None
            if metrics and 'metric' in metrics:
                vol_10d = metrics['metric'].get('10DayAverageTradingVolume')
            
            # Parse insider (look for positive MSPR - Management Sentiment)
            insider_score = 0
            if insider_data and 'data' in insider_data and len(insider_data['data']) > 0:
                # Sum the monthly sentiment scores (mspr)
                insider_score = sum([month.get('mspr', 0) for month in insider_data['data']])
                insider_score = round(insider_score, 2)

            # We won't have real-time volume in this basic script without hitting /quote, but we can flag high insider buying
            
            sentiment_flag = "🟢 STRONG INSIDER BUYING" if insider_score > 5 else ("🔴 INSIDER SELLING" if insider_score < -5 else "⚪ NEUTRAL")
            
            print(f"  {sym:<5} | Insider Sentiment Score: {insider_score:>6} | {sentiment_flag}")

    print("==================================================================")
    print(" SCAN COMPLETE. Check for cluster buying and volume divergence.   ")
    print("==================================================================")

if __name__ == "__main__":
    main()