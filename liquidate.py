import urllib.request
import json
import time

# Use credentials from TOOLS.md
API_KEY = "PKLXTM37LF7Y4PUXRKAUAJEWC5"
SECRET_KEY = "Evk5W9HHZc9ZmB8jbqKE52KGE6SNWoy5hXSrLHvCaDCq"
BASE_URL = "https://paper-api.alpaca.markets/v2"

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
    "Content-Type": "application/json"
}

def liquidate_all():
    print("Fetching positions...")
    req = urllib.request.Request(f"{BASE_URL}/positions", headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            positions = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
        return

    for pos in positions:
        print(f"Selling {pos['symbol']}...")
        order_data = {
            "symbol": pos['symbol'],
            "qty": pos['qty'],
            "side": "sell",
            "type": "market",
            "time_in_force": "day"
        }
        req = urllib.request.Request(f"{BASE_URL}/orders", data=json.dumps(order_data).encode('utf-8'), headers=HEADERS)
        try:
            urllib.request.urlopen(req)
            print("Submitted.")
        except Exception as e:
            print(f"Failed: {e}")
        time.sleep(2)

liquidate_all()
