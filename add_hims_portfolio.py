import urllib.request
import json

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwduupbK9co0SSHoSAVkRcRlNU_mlxFyjQMcVfRXJ11Dam8xd12ZQUj2TtGFaizr6S2xA/exec"

def push_to_sheets(trade_dict):
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(trade_dict).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

t = {
    "sheet_name": "Portfolio",
    "date": "2026-03-10",
    "ticker": "HIMS",
    "action": "BUY",
    "shares": 451,
    "price": 22.17,
    "total": 9998.67,
    "category": "Growth",
    "confidence": "90%",
    "invalidation": 18.50,
    "pl_usd": 0,
    "pl_pct": 0,
    "status": "OPEN"
}

res = push_to_sheets(t)
print(f"Status: {res}")
