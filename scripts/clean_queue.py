import urllib.request
import json

API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
    "Content-Type": "application/json"
}

def cancel_all_orders():
    # DELETE all orders
    req = urllib.request.Request(f"{BASE_URL}/v2/orders", headers=HEADERS, method='DELETE')
    with urllib.request.urlopen(req) as response:
        return "All orders cancelled"

# Cancel everything so we start clean
print(cancel_all_orders())
