import urllib.request
import json

API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

try:
    req = urllib.request.Request(f"{BASE_URL}/v2/positions")
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    with urllib.request.urlopen(req) as response:
        positions = json.loads(response.read().decode('utf-8'))
        for p in positions:
            print(f"Symbol: {p['symbol']}, Qty: {p['qty']}")
except Exception as e:
    print(f"Error: {e}")
