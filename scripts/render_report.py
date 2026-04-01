import json

with open('/home/warwick/.openclaw/workspace/audit_results_2025.json', 'r') as f:
    data = json.load(f)

# Simulation Logic
def simulate_portfolio(vectors, start_capital=10000):
    balance = start_capital
    history = []
    for v in vectors:
        balance = balance * (1 + (v['return'] / 100))
        history.append(round(balance, 2))
    return history

html = """
<html>
<head>
    <style>
        body { font-family: 'Helvetica', sans-serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 40px; }
        h1 { border-bottom: 3px solid #1a2a6c; color: #1a2a6c; padding-bottom: 10px; }
        .stat-box { background: #e8f0fe; padding: 20px; margin: 20px 0; border-left: 5px solid #1a2a6c; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.9em; }
        th, td { border: 1px solid #000; padding: 10px; text-align: center; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>Atlas Alpha: 2025 Compounding Audit</h1>
    <p>This simulation assumes an initial $10,000 starting capital per index, with 100% of available capital rotated into each detected "Earnings Drift" vector.</p>
"""

for index, vectors in data.items():
    history = simulate_portfolio(vectors)
    final_val = history[-1]
    total_ret = ((final_val / 10000) - 1) * 100
    
    html += f"<h2>{index} Performance Simulation</h2>"
    html += f"""
    <div class="stat-box">
        <h3>Capital Compounding: Initial $10,000</h3>
        <p>Final Portfolio Value: <strong>${final_val:,.2f}</strong></p>
        <p>Total Cumulative Return: <strong>{total_ret:.2f}%</strong></p>
    </div>
    <table>
        <tr><th>Ticker</th><th>Date</th><th>Entry Price</th><th>Result</th><th>Cumulative Balance</th></tr>
    """
    
    balance = 10000
    for v in vectors:
        balance = balance * (1 + (v['return'] / 100))
        status = "Invalidated" if v['invalidated'] else "Success"
        html += f"<tr><td>{v['symbol']}</td><td>{v['date']}</td><td>${v['entry']:.2f}</td><td>{status}</td><td>${balance:,.2f}</td></tr>"
    html += "</table>"

html += "</body></html>"

with open('/home/warwick/.openclaw/workspace/PERFORMANCE_AUDIT_2025_FORMAL.html', 'w') as f:
    f.write(html)
