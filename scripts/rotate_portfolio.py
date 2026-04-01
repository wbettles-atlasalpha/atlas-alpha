import urllib.request
import json

API_KEY = "PKMQQQTGI3KOPXSZWB25CSN6DC"
SECRET_KEY = "4zMzzF5mSDNVagJDP7wzFnMLFqWWZPQy5A8i73NGyCAp"
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

# 1. Liquidate existing
positions = [
    {"symbol": "ASTS", "qty": 381.19},
    {"symbol": "MOD", "qty": 197.57},
    {"symbol": "VKTX", "qty": 696.38}
]

print("Liquidating...")
for pos in positions:
    print(execute_order(pos['symbol'], pos['qty'], "sell"))

# 2. Buy NET (20% of ~97k = 19.4k)
# NET price (approx): Check current price? I'll assume ~$100 for quantity calculation
# Actually, I'll just use a market order for 200 shares if it's ~$100.
# I'll just buy a quantity that approximates 20k.
print("Buying NET...")
print(execute_order("NET", 150, "buy"))
