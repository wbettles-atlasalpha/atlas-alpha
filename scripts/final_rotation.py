import urllib.request
import json

# New credentials
API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

def execute_order(symbol, qty, side, order_type="market"):
    order_data = {
        "symbol": symbol,
        "qty": str(qty),
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

def get_positions():
    req = urllib.request.Request(f"{BASE_URL}/v2/positions")
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

try:
    print("Testing Auth and Liquidation...")
    # 1. Liquidate all existing
    for pos in get_positions():
        print(f"Liquidating {pos['symbol']}...")
        print(execute_order(pos['symbol'], pos['qty'], "sell"))

    # 2. Buy NET (200 shares)
    print("Buying NET...")
    print(execute_order("NET", "200", "buy"))

except Exception as e:
    print(f"Error: {e}")
