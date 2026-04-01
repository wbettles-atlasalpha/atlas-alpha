import json
import urllib.request
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwdlDuwdcXZcY9dtVnhOdYNeTy39zRoRxMRriYk5IKgD6-g-qYYkiAwPKzZtYT9UZ03sA/exec"

def push_to_sheets(trade):
    # Mapping based on the appendRow call in doPost(e):
    # sheet.appendRow([data.date, data.ticker, data.action, data.shares, data.price, data.total, data.category, data.confidence, data.invalidation, 0, 0, "OPEN"]);
    
    payload = {
        "sheet_name": "Portfolio",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "ticker": trade.get("ticker"),
        "action": trade.get("action"),
        "shares": trade.get("size"),
        "price": trade.get("price"),
        "total": trade.get("size") * trade.get("price"),
        "category": trade.get("category", "Master Strategy Vector"),
        "confidence": 90, # Explicitly setting to 90 as per instruction
        "invalidation": round(trade.get("price") * 0.95, 2)
    }
    
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"
