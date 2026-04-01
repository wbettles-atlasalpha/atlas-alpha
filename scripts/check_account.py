import urllib.request
import json

API_KEY = "PKMQQQTGI3KOPXSZWB25CSN6DC"
SECRET_KEY = "4zMzzF5mSDNVagJDP7wzFnMLFqWWZPQy5A8i73NGyCAp"
BASE_URL = "https://paper-api.alpaca.markets"

req = urllib.request.Request(f"{BASE_URL}/v2/account")
req.add_header("APCA-API-KEY-ID", API_KEY)
req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
with urllib.request.urlopen(req) as response:
    print(response.read().decode('utf-8'))
