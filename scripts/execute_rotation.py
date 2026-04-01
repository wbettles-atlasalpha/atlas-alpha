import requests

# Alpaca Paper Trading Credentials from TOOLS.md
API_KEY = "PKLXTM37LF7Y4PUXRKAUAJEWC5"
SECRET_KEY = "Evk5W9HHZc9ZmB8jbqKE52KGE6SNWoy5hXSrLHvCaDCq"
BASE_URL = "https://paper-api.alpaca.markets/v2"

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
    "Content-Type": "application/json"
}

def get_positions():
    response = requests.get(f"{BASE_URL}/positions", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def liquidate_all():
    positions = get_positions()
    for pos in positions:
        if pos['symbol'] in ['PME.AX', 'JBH.AX']:
            print(f"Liquidating {pos['symbol']}...")
            data = {
                "symbol": pos['symbol'],
                "qty": pos['qty'],
                "side": "sell",
                "type": "market",
                "time_in_force": "day"
            }
            response = requests.post(f"{BASE_URL}/orders", headers=headers, json=data)
            print(f"Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    liquidate_all()
