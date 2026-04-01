import urllib.request
import json

# Verified Keys
API_KEY = "PKDCJ4OSJOIUW5A32QU7BCJIFT"
SECRET_KEY = "E7AtTQ8i8ovmpMyjnDacEececvrhDYqVa3vprPcRu1V3"
BASE_URL = "https://paper-api.alpaca.markets"

def sell_position(symbol, qty):
    print(f"Selling {symbol} with qty {qty}...")
    order_data = {
        "symbol": symbol,
        "qty": str(qty), # Cast to string
        "side": "sell",
        "type": "market",
        "time_in_force": "gtc"
    }
    req = urllib.request.Request(
        f"{BASE_URL}/v2/orders", 
        data=json.dumps(order_data).encode('utf-8'),
        method='POST',
        headers={
            "APCA-API-KEY-ID": API_KEY,
            "APCA-API-SECRET-KEY": SECRET_KEY,
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Response: {response.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error selling {symbol}: {e}")

# Exact quantities from my previous check:
# Symbol: ASTS, Qty: 0.001364083
# Symbol: MOD, Qty: 197.569890349
# Symbol: VKTX, Qty: 696.378830084

if __name__ == "__main__":
    sell_position("MOD", 197.569890349)
    sell_position("VKTX", 696.378830084)
    sell_position("ASTS", 0.001364083) # Might fail if too small, but let's see.
