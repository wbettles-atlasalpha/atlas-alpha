import requests
import json
import time

API_KEY = "PKLXTM37LF7Y4PUXRKAUAJEWC5"
SECRET_KEY = "Evk5W9HHZc9ZmB8jbqKE52KGE6SNWoy5hXSrLHvCaDCq"
BASE_URL = "https://paper-api.alpaca.markets/v2"

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

def get_portfolio_status():
    url = f"{BASE_URL}/positions"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        positions = response.json()
        return positions
    else:
        print(f"Error checking positions: {response.status_code}")
        return []

if __name__ == "__main__":
    positions = get_portfolio_status()
    if not positions:
        print("Portfolio is currently flat (no open positions).")
    else:
        for pos in positions:
            print(f"{pos['symbol']}: {pos['qty']} shares @ {pos['avg_entry_price']} (Unrealized P&L: {pos['unrealized_pl']})")
