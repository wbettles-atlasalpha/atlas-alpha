import urllib.request

API_KEY = "PK6JBCU3CLUWQKV44RQT75EHPB"
SECRET_KEY = "D6S6FCqqouRVr5ycUgbpWMsFAUNd4yNBnCwKM3PS57A3"
BASE_URL = "https://paper-api.alpaca.markets"

try:
    req = urllib.request.Request(f"{BASE_URL}/v2/account")
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
