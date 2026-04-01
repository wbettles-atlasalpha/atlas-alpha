import urllib.request
import json

# Verified Keys
API_KEY = "PKDCJ4OSJOIUW5A32QU7BCJIFT"
SECRET_KEY = "E7AtTQ8i8ovmpMyjnDacEececvrhDYqVa3vprPcRu1V3"
BASE_URL = "https://paper-api.alpaca.markets"

def close_position(symbol):
    print(f"Attempting to close {symbol}...")
    req = urllib.request.Request(f"{BASE_URL}/v2/positions/{symbol}", method='DELETE')
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    try:
        with urllib.request.urlopen(req) as res:
            print(f"Closed {symbol}: {res.status}")
    except Exception as e:
        print(f"Error closing {symbol}: {e}")

if __name__ == "__main__":
    close_position("ASTS")
    close_position("MOD")
    close_position("VKTX")
