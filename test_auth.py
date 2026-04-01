import urllib.request

API_KEY = "AKQWQU2E74Q5HEMO5J5QZ5RL43"
SECRET_KEY = "Ew5879YiXDDaJTdiArQnRFCL3Mf5YYof5fPwzn3CBMiN"
BASE_URL = "https://paper-api.alpaca.markets"

try:
    req = urllib.request.Request(f"{BASE_URL}/v2/account")
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
