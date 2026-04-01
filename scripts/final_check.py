import urllib.request
import json

# Check the exact scope of the API key provided
API_KEY = "PKWOAAACI6MHQCJQSYHNU7FY6R"
SECRET_KEY = "F8QNzPRcAmfLyFBg6WMX4nBcEX6u9BhMJV8s4NMi7noB"
BASE_URL = "https://paper-api.alpaca.markets"

# Check Account details again
req = urllib.request.Request(f"{BASE_URL}/v2/account")
req.add_header("APCA-API-KEY-ID", API_KEY)
req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)

try:
    with urllib.request.urlopen(req) as response:
        account = json.loads(response.read().decode('utf-8'))
        # This will tell us if trading is blocked at the account level
        print(f"Trading Blocked: {account['trading_blocked']}")
        print(f"Account Status: {account['status']}")
except Exception as e:
    print(f"Error: {e}")
