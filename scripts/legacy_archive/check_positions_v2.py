import urllib.request
import json

API_KEY = "PKMQQQTGI3KOPXSZWB25CSN6DC"
SECRET_KEY = "4zMzzF5mSDNVagJDP7wzFnMLFqWWZPQy5A8i73NGyCAp"
BASE_URL = "https://paper-api.alpaca.markets"

try:
    req = urllib.request.Request(f"{BASE_URL}/v2/positions")
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    
    with urllib.request.urlopen(req) as response:
        positions = json.loads(response.read().decode('utf-8'))
        if not positions:
            print("No open positions found.")
        for p in positions:
            print(f"Symbol: {p['symbol']}, Qty: {p['qty']}, Avg Entry: {p['avg_entry_price']}")
except Exception as e:
    print(f"Error: {e}")
