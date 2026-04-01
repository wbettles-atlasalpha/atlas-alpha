import json

with open("PORTFOLIO_STATE.json", "r") as f:
    state = json.load(f)

cash_spent = 9998.67
state["current_cash_usd"] -= cash_spent
state["equity_usd"] += cash_spent
state["open_positions"].append("HIMS")

with open("PORTFOLIO_STATE.json", "w") as f:
    json.dump(state, f, indent=2)

with open("PORTFOLIO_LEDGER.csv", "a") as f:
    f.write("2026-03-10,HIMS,BUY,451,22.17,9998.67,Growth,90%,18.50,0,0,OPEN\n")

print("Local state updated")
