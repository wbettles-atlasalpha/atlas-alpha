import urllib.request
import json
import time

# Final Throttled Rotation Script
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

# Execution Queue
orders = [
    ("ASTS", 381.19, "sell"),
    ("MOD", 197.57, "sell"),
    ("VKTX", 696.38, "sell"),
    ("NET", 88.89, "buy"),
    ("FDX", 68.97, "buy")
]

for sym, qty, side in orders:
    print(f"Submitting {side} order for {sym}...")
    try:
        print(execute_order(sym, qty, side))
        # 30-second delay between orders to ensure we don't trigger the API lockout
        time.sleep(30)
    except Exception as e:
        print(f"Error executing {sym}: {e}")
        # Stop on error to prevent cascading fails
        break
