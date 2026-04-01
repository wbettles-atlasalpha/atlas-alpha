import sys
import json
import urllib.request

# The Google App Script handles "DELETE" or "CLEAR" based on the request type if structured correctly.
# Assuming a standard update-to-sheet flow where I can send a command.
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyWVbrJlBpmX6TMY3nUbqgvooFmXsQtV2s5mxubrGZfXa4762HQ9Ur17NV1_LO_9198gw/exec"

def clear_ledger_entry(ticker):
    payload = {
        "Ticker": ticker,
        "Action": "DELETE"
    }
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

print(f"Removing TTD...")
print(clear_ledger_entry("TTD"))
