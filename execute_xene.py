import urllib.request
import json
import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyWVbrJlBpmX6TMY3nUbqgvooFmXsQtV2s5mxubrGZfXa4762HQ9Ur17NV1_LO_9198gw/exec"

def push_to_sheets(trade_dict):
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(trade_dict).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

# 1. Push to Portfolio
portfolio_trade = {
    "sheet_name": "Portfolio",
    "date": "2026-03-10",
    "ticker": "XENE",
    "action": "BUY",
    "shares": 71,
    "price": 62.76,
    "total": 4455.96,
    "category": "Growth",
    "confidence": "85%",
    "invalidation": 55.00
}

res_port = push_to_sheets(portfolio_trade)
print(f"Portfolio Push: {res_port}")

# 2. Push to Signals
signal_trade = {
    "sheet_name": "Signals",
    "date": "2026-03-10",
    "masked_name": "Neurology Biotech Breakout",
    "real_ticker": "XENE",
    "category": "Growth",
    "confidence": "85%",
    "entry": 62.76,
    "thesis": "Massive +49% gap up on 10x relative volume, indicating major institutional accumulation likely off tier-1 clinical data. Clean momentum breakout.",
    "invalidation_text": "Break below $55.00"
}

res_sig = push_to_sheets(signal_trade)
print(f"Signals Push: {res_sig}")

# Update Local State
try:
    with open("PORTFOLIO_STATE.json", "r") as f:
        state = json.load(f)
    state["open_positions"].append("XENE")
    with open("PORTFOLIO_STATE.json", "w") as f:
        json.dump(state, f, indent=2)
except Exception as e:
    print("State JSON error:", e)

with open("PORTFOLIO_LEDGER.csv", "a") as f:
    f.write(f"2026-03-10,XENE,BUY,71,62.76,4455.96,Growth,85%,55.00,0,0,OPEN\n")

