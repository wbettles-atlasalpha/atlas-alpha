import urllib.request
import json

# Correct keys from Warwick
API_KEY = "PKMQQQTGI3KOPXSZWB25CSN6DC"
# Note: I need the secret. I will assume the secret is the one I have on record in TOOLS.md if not provided, but Warwick said "associated secret". 
# Wait, I do not have the secret for this new key. 
# I will ask Warwick to provide the secret if the old one doesn't work, but I'll try the old one just in case.
SECRET_KEY = "Ew5879YiXDDaJTdiArQnRFCL3Mf5YYof5fPwzn3CBMiN" 
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
