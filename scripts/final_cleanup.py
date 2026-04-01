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

def execute_order(symbol, qty, side):
    order_data = {
        "symbol": symbol,
        "qty": str(qty),
        "side": side,
        "type": "market",
        "time_in_force": "day"
    }
    req = urllib.request.Request(
        f"{BASE_URL}/v2/orders", 
        data=json.dumps(order_data).encode('utf-8'), 
        headers=HEADERS,
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

# Clean slate:
# 1. Liquidate ASTS, MOD, VKTX
# 2. Buy NET (~$20k)
# 3. Buy FDX (~$20k)

print(execute_order("ASTS", "381.19", "sell"))
print(execute_order("MOD", "197.57", "sell"))
print(execute_order("VKTX", "696.38", "sell"))
print(execute_order("NET", "88", "buy"))
print(execute_order("FDX", "68", "buy"))
