import urllib.request
import json

API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

# Add User-Agent to prevent 403 block
HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AtlasAlphaBot/1.0"
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

try:
    print("Testing Sell Order (Test)...")
    # Sell a tiny bit of ASTS (0.01) to test if POST works
    print(execute_order("ASTS", "0.01", "sell"))
except Exception as e:
    print(f"Error: {e}")
