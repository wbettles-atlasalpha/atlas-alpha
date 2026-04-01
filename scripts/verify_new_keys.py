import requests
import json

# New credentials provided by Warwick
API_KEY = "PKDCJ4OSJOIUW5A32QU7BCJIFT"
SECRET_KEY = "E7AtTQ8i8ovmpMyjnDacEececvrhDYqVa3vprPcRu1V3"
BASE_URL = "https://paper-api.alpaca.markets"

# Setup persistent session
session = requests.Session()
session.headers.update({
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
})

def verify_credentials():
    try:
        response = session.get(f"{BASE_URL}/v2/account")
        if response.status_code == 200:
            account = response.json()
            print("Successfully verified new API credentials.")
            print(f"Buying Power: ${account['buying_power']}")
            return True
        else:
            print(f"Verification Failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error connecting: {e}")
        return False

if __name__ == "__main__":
    verify_credentials()
