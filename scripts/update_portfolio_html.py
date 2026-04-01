import csv

# Assuming you want to read from PORTFOLIO_LEDGER.csv
# and update/generate an HTML table
with open('/home/warwick/.openclaw/workspace/PORTFOLIO_LEDGER.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

html = """
<html>
<head>
    <style>
        body { font-family: sans-serif; padding: 40px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #000; padding: 8px; text-align: center; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>Atlas Alpha: Current Portfolio</h1>
    <table>
        <tr><th>Ticker</th><th>Entry Price</th><th>Current Price</th><th>P/L</th></tr>
"""

for row in rows:
    html += f"<tr><td>{row['ticker']}</td><td>${float(row['entry_usd']):.2f}</td><td>${float(row['current_usd']):.2f}</td><td>{row['pl_pct']}%</td></tr>"

html += "</table></body></html>"

with open('/home/warwick/.openclaw/workspace/CURRENT_PORTFOLIO.html', 'w') as f:
    f.write(html)
