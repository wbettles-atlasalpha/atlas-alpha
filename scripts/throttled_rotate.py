import time
import urllib.request
import json

# Institutional Strategy execution
# Rotate ASTS, MOD, VKTX to NET and FDX
# One order at a time with a delay.

API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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

# Operations
orders = [
    ("ASTS", 381.19, "sell"),
    ("MOD", 197.57, "sell"),
    ("VKTX", 696.38, "sell"),
    ("NET", 88, "buy"),
    ("FDX", 68, "buy")
]

for sym, qty, side in orders:
    print(f"Submitting {side} order for {sym}...")
    try:
        print(execute_order(sym, qty, side))
        time.sleep(5) # Throttle to avoid 403 rate limits/bot detection
    except Exception as e:
        print(f"Error executing {sym}: {e}")
        break
