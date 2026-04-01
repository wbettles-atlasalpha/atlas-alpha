import urllib.request
import json
import time

API_KEY = "PK6JBCU3CLUWQKV44RQT75EHPB"
SECRET_KEY = "D6S6FCqqouRVr5ycUgbpWMsFAUNd4yNBnCwKM3PS57A3"
BASE_URL = "https://paper-api.alpaca.markets"

trades = [
    {"symbol": "NVDA", "qty": 109.5},
    {"symbol": "PLTR", "qty": 127.85},
    {"symbol": "RKLB", "qty": 209.85},
    {"symbol": "CRWD", "qty": 34.55},
    {"symbol": "UBER", "qty": 203.14},
    {"symbol": "MRVL", "qty": 111},
    {"symbol": "SWBI", "qty": 714},
    {"symbol": "DAWN", "qty": 235},
    {"symbol": "HIMS", "qty": 451}
]

for t in trades:
    order_data = {
        "symbol": t["symbol"],
        "qty": t["qty"],
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
            print(f"[{t['symbol']}] Status: {result.get('status')} | ID: {result.get('id')}")
    except Exception as e:
        print(f"[{t['symbol']}] Error: {e}")
    time.sleep(1) # Rate limit safety
