import requests
import json
import os

API_KEY = "PKLXTM37LF7Y4PUXRKAUAJEWC5"
SECRET_KEY = "Evk5W9HHZc9ZmB8jbqKE52KGE6SNWoy5hXSrLHvCaDCq"
BASE_URL = "https://paper-api.alpaca.markets/v2"

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

def fetch_active_tickers():
    url = f"{BASE_URL}/assets?status=active&asset_class=us_equity"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        assets = response.json()
        # Filter for tradable, marginable, and common stock
        tickers = [a['symbol'] for a in assets if a['tradable'] and a['marginable'] and a['symbol'].isalpha()]
        # Limit to top 200 to keep scan fast
        return tickers[:200]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    tickers = fetch_active_tickers()
    with open('/home/warwick/.openclaw/workspace/data/tickers.json', 'w') as f:
        json.dump(tickers, f)
    print(f"Successfully saved {len(tickers)} tickers.")
