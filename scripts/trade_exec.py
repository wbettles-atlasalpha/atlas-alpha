import urllib.request
import json
import sys

API_KEY = "PKDCJ4OSJOIUW5A32QU7BCJIFT"
SECRET_KEY = "E7AtTQ8i8ovmpMyjnDacEececvrhDYqVa3vprPcRu1V3"
BASE_URL = "https://paper-api.alpaca.markets"

def execute_order(symbol, qty, side, order_type="market"):
    order_data = {
        "symbol": symbol,
        "qty": qty,
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

# Buy $10,000 worth of ASTS (~111 shares @ $90)
print("Executing ASTS Buy...")
print(execute_order("ASTS", 111, "buy"))
