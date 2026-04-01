import urllib.request
import json

API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

req = urllib.request.Request(f"{BASE_URL}/v2/orders?status=open")
req.add_header("APCA-API-KEY-ID", API_KEY)
req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
with urllib.request.urlopen(req) as response:
    orders = json.loads(response.read().decode('utf-8'))
    for o in orders:
        print(f"Open Order: {o['symbol']}, Qty: {o['qty']}, Side: {o['side']}")
