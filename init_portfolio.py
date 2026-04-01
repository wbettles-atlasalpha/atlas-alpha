import urllib.request
import json
import time

API_KEY = "PK6JBCU3CLUWQKV44RQT75EHPB"
SECRET_KEY = "D6S6FCqqouRVr5ycUgbpWMsFAUNd4yNBnCwKM3PS57A3"
BASE_URL = "https://paper-api.alpaca.markets"

picks = [
    {"symbol": "MOD", "qty": 202},
    {"symbol": "ASTS", "qty": 392},
    {"symbol": "VKTX", "qty": 694}
]

for p in picks:
    order_data = {
        "symbol": p["symbol"],
        "qty": p["qty"],
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
            print(f"[{p['symbol']}] Success")
    except Exception as e:
        print(f"[{p['symbol']}] Error: {e}")
    time.sleep(2)
