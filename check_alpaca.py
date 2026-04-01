import urllib.request
import json

API_KEY = "PKLXTM37LF7Y4PUXRKAUAJEWC5"
SECRET_KEY = "Evk5W9HHZc9ZmB8jbqKE52KGE6SNWoy5hXSrLHvCaDCq"
BASE_URL = "https://paper-api.alpaca.markets"

try:
    req = urllib.request.Request(f"{BASE_URL}/v2/positions")
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    
    with urllib.request.urlopen(req) as response:
        positions = json.loads(response.read().decode('utf-8'))
        print(json.dumps(positions, indent=2))
except Exception as e:
    print(f"Error: {e}")
