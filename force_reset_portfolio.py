import urllib.request
import json
import time

API_KEY = "PK6JBCU3CLUWQKV44RQT75EHPB"
SECRET_KEY = "D6S6FCqqouRVr5ycUgbpWMsFAUNd4yNBnCwKM3PS57A3"
BASE_URL = "https://paper-api.alpaca.markets"

def liquidate():
    # 1. Get current positions
    req = urllib.request.Request(f"{BASE_URL}/v2/positions")
    req.add_header("APCA-API-KEY-ID", API_KEY)
    req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
    
    with urllib.request.urlopen(req) as response:
        positions = json.loads(response.read().decode('utf-8'))

    if not positions:
        print("No positions to liquidate.")
        return

    # 2. Sell everything
    for pos in positions:
        print(f"Liquidating {pos['symbol']}...")
        order_data = {
            "symbol": pos['symbol'],
            "qty": pos['qty'],
            "side": "sell",
            "type": "market",
            "time_in_force": "day"
        }
        
        req = urllib.request.Request(f"{BASE_URL}/v2/orders", data=json.dumps(order_data).encode('utf-8'))
        req.add_header("APCA-API-KEY-ID", API_KEY)
        req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
        req.add_header("Content-Type", "application/json")
        
        try:
            with urllib.request.urlopen(req) as response:
                print(f"[{pos['symbol']}] Order accepted")
        except Exception as e:
            print(f"[{pos['symbol']}] Error: {e}")
        time.sleep(1)

    # 3. Reset local state files
    open("/home/warwick/.openclaw/workspace/PORTFOLIO_STATE.json", "w").write("{}")
    open("/home/warwick/.openclaw/workspace/PORTFOLIO_LEDGER.csv", "w").write("date,ticker,action,shares,entry_usd,current_usd,total_cost,category,confidence,invalidation,pl_usd,pl_pct,status\n")

liquidate()
