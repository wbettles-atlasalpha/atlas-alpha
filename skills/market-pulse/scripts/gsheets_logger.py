import urllib.request
import json
import sys

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyWVbrJlBpmX6TMY3nUbqgvooFmXsQtV2s5mxubrGZfXa4762HQ9Ur17NV1_LO_9198gw/exec"

def push_to_sheets(trade_dict):
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(trade_dict).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Use push_to_sheets(trade_dict) directly.")
