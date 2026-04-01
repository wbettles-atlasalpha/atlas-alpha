import urllib.request
import json

API_KEY = "PKMQQQTGI3KOPXSZWB25CSN6DC"
SECRET_KEY = "4zMzzF5mSDNVagJDP7wzFnMLFqWWZPQy5A8i73NGyCAp"
BASE_URL = "https://paper-api.alpaca.markets"

def execute_order(symbol, qty, side, order_type="market"):
    order_data = {
        "symbol": symbol,
        "qty": str(qty), # Must be string
        "side": side,
        "type": order_type,
        "time_in_force": "day"
    }
    req = urllib.request.Request(f"{BASE_URL}/v2/orders", data=json.dumps(order_data).encode('utf-8'))
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

print("Attempting test buy...")
print(execute_order("NET", "1", "buy"))
