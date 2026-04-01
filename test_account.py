import urllib.request, json

KEY    = "PKLXTM37LF7Y4PUXRKAUAJEWC5"
SECRET = "Evk5W9HHZc9ZmB8jbqKE52KGE6SNWoy5hXSrLHvCaDCq"
BASE   = "https://paper-api.alpaca.markets"

def get_account():
    req = urllib.request.Request(
        f"{BASE}/v2/account",
        headers={"APCA-API-KEY-ID": KEY, "APCA-API-SECRET-KEY": SECRET}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

try:
    print(get_account())
except Exception as e:
    print(f"Error: {e}")
