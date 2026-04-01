import urllib.request
import json
import csv

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyaZbCRiqvX1IEBFIC6UvNXRKVvQBpVlEjC2IYh4RHeyAgdb6e2zsf48f7nzFDww6Y5ZA/exec"

def push_to_sheets(trade_dict):
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(trade_dict).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

trades = [
    {"date":"2026-03-09", "ticker":"NVDA", "action":"BUY", "shares":109.5, "price":182.65, "total":109.5*182.65, "category":"Core", "confidence":"95%", "invalidation":165.00, "pl_usd":0, "pl_pct":0, "status":"OPEN"},
    {"date":"2026-03-09", "ticker":"PLTR", "action":"BUY", "shares":127.85, "price":156.43, "total":127.85*156.43, "category":"Growth", "confidence":"90%", "invalidation":138.50, "pl_usd":0, "pl_pct":0, "status":"OPEN"},
    {"date":"2026-03-09", "ticker":"RKLB", "action":"BUY", "shares":209.85, "price":71.48, "total":209.85*71.48, "category":"Moonshot", "confidence":"85%", "invalidation":55.00, "pl_usd":0, "pl_pct":0, "status":"OPEN"},
    {"date":"2026-03-10", "ticker":"CRWD", "action":"BUY", "shares":34.55, "price":434.13, "total":34.55*434.13, "category":"Core", "confidence":"90%", "invalidation":395.00, "pl_usd":0, "pl_pct":0, "status":"OPEN"},
    {"date":"2026-03-10", "ticker":"UBER", "action":"BUY", "shares":203.14, "price":73.84, "total":203.14*73.84, "category":"Value/Growth", "confidence":"85%", "invalidation":64.50, "pl_usd":0, "pl_pct":0, "status":"OPEN"}
]

for t in trades:
    t["sheet_name"] = "Portfolio"
    res = push_to_sheets(t)
    print(f"[{t['ticker']}] Webhook Status: {res}")

# Update Local State
with open("PORTFOLIO_STATE.json", "r") as f:
    state = json.load(f)

for t in trades:
    state["open_positions"].append(t["ticker"])
    # Not subtracting from cash since they were already assumed part of the old state, but let's check.
    # Actually, we should just append them to the ledger.
    with open("PORTFOLIO_LEDGER.csv", "a") as f:
        f.write(f"{t['date']},{t['ticker']},BUY,{t['shares']},{t['price']},{t['total']:.2f},{t['category']},{t['confidence']},{t['invalidation']},0,0,OPEN\n")

with open("PORTFOLIO_STATE.json", "w") as f:
    json.dump(state, f, indent=2)

print("Backend state updated!")
