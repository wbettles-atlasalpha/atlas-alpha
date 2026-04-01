import urllib.request
import json

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyaZbCRiqvX1IEBFIC6UvNXRKVvQBpVlEjC2IYh4RHeyAgdb6e2zsf48f7nzFDww6Y5ZA/exec"

def push_to_sheets(trade_dict):
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(trade_dict).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

t = {
    "sheet_name": "Signals",
    "date": "2026-03-10",
    "masked_name": "Telehealth Disruptor",
    "real_ticker": "HIMS",
    "category": "Growth",
    "confidence": "90%",
    "entry": 22.17,
    "thesis": "Huge volume anomaly (5.48x average) showing significant momentum breakout.",
    "invalidation_text": "Break below $18.50"
}

res = push_to_sheets(t)
print(f"Status: {res}")
