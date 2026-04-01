import urllib.request
import json

API_KEY = "PK6JBCU3CLUWQKV44RQT75EHPB"
SECRET_KEY = "D6S6FCqqouRVr5ycUgbpWMsFAUNd4yNBnCwKM3PS57A3"
BASE_URL = "https://paper-api.alpaca.markets"

order_data = {
    "symbol": "XENE",
    "qty": 71,
    "side": "buy",
    "type": "market",
    "time_in_force": "day"
}

try:
    req = urllib.request.Request(f"{BASE_URL}/v2/orders", data=json.dumps(order_data).encode('utf-8'))
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    req.add_header("Content-Type", "application/json")
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Order ID: {result.get('id')}")
        print(f"Status: {result.get('status')}")
        print(f"Symbol: {result.get('symbol')}")
        print(f"Qty: {result.get('qty')}")
except Exception as e:
    print(f"Error: {e}")
