import requests
import time

API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

# Use a persistent session
session = requests.Session()
session.headers.update({
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

def execute_order(symbol, qty, side):
    data = {"symbol": symbol, "qty": str(qty), "side": side, "type": "market", "time_in_force": "day"}
    return session.post(f"{BASE_URL}/v2/orders", json=data)

# Execution: Clear legacy, start drift
orders = [
    ("ASTS", 381.19, "sell"),
    ("MOD", 197.57, "sell"),
    ("VKTX", 696.38, "sell"),
    ("NET", 88.89, "buy")
]

for sym, qty, side in orders:
    print(f"Submitting {side} {sym}...")
    resp = execute_order(sym, qty, side)
    if resp.status_code == 200:
        print(f"Success: {resp.json()['id']}")
    else:
        print(f"Failed {sym}: {resp.status_code} {resp.text}")
    time.sleep(5)
