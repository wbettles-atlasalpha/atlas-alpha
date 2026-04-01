import urllib.request
import json

API_KEY = "PKMQQQTGI3KOPXSZWB25CSN6DC"
SECRET_KEY = "4zMzzF5mSDNVagJDP7wzFnMLFqWWZPQy5A8i73NGyCAp"
BASE_URL = "https://paper-api.alpaca.markets"

# Try closing ASTS specifically via DELETE
req = urllib.request.Request(f"{BASE_URL}/v2/positions/ASTS?qty=381.19", method='DELETE')
req.add_header("APCA-API-KEY-ID", API_KEY)
req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
