import json
import os
from datetime import datetime

# State File
SIM_PORTFOLIO_FILE = 'SIM_PORTFOLIO.json'

def load_portfolio():
    if not os.path.exists(SIM_PORTFOLIO_FILE):
        return {"cash": 100000.0, "positions": {}, "transactions": [], "last_updated": str(datetime.now().date())}
    with open(SIM_PORTFOLIO_FILE, 'r') as f:
        return json.load(f)

def save_portfolio(portfolio):
    portfolio['last_updated'] = str(datetime.now().date())
    with open(SIM_PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=4)
    generate_html_report(portfolio)

def execute_trade(symbol, qty, side, price):
    p = load_portfolio()
    cost = qty * price
    
    if side == "buy":
        if p['cash'] >= cost:
            p['cash'] -= cost
            p['positions'][symbol] = p['positions'].get(symbol, 0) + qty
        else:
            print("Insufficient cash.")
            return
    elif side == "sell":
        if p['positions'].get(symbol, 0) >= qty:
            p['cash'] += cost
            p['positions'][symbol] -= qty
        else:
            print("Insufficient position.")
            return
            
    p['transactions'].append({
        "symbol": symbol, 
        "qty": qty, 
        "side": side, 
        "price": price, 
        "date": str(datetime.now())
    })
    save_portfolio(p)
    print(f"Executed {side} {symbol} @ {price}")

def generate_html_report(portfolio):
    html_content = f"""
    <html>
    <head><title>Atlas Alpha Simulation</title></head>
    <body>
        <h1>Portfolio Status (as of {portfolio['last_updated']})</h1>
        <p>Cash: ${portfolio['cash']:.2f}</p>
        <h2>Positions</h2>
        <table border="1">
            <tr><th>Symbol</th><th>Qty</th></tr>
            {''.join(f"<tr><td>{sym}</td><td>{qty}</td></tr>" for sym, qty in portfolio['positions'].items())}
        </table>
        <h2>Recent Transactions</h2>
        <table border="1">
            <tr><th>Date</th><th>Symbol</th><th>Side</th><th>Qty</th><th>Price</th></tr>
            {''.join(f"<tr><td>{t['date']}</td><td>{t['symbol']}</td><td>{t['side']}</td><td>{t['qty']}</td><td>{t['price']}</td></tr>" for t in portfolio['transactions'][-10:])}
        </table>
    </body>
    </html>
    """
    with open('portfolio.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    # Example logic: deploy cash based on signal
    # execute_trade("XLE", 200, "buy", 100.0) # Placeholder
    pass
