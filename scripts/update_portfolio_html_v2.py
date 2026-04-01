import csv

# Current portfolio state as per manual user input
portfolio_data = [
    {"Ticker": "XLE", "Allocation": "35%", "Invested": "$35,000", "Current Value": "$35,000", "P/L ($)": "$0", "P/L (%)": "0.0%", "Role": "Energy Hedge"},
    {"Ticker": "XLP", "Allocation": "30%", "Invested": "$30,000", "Current Value": "$30,000", "P/L ($)": "$0", "P/L (%)": "0.0%", "Role": "Consumer Staples"},
    {"Ticker": "XLV", "Allocation": "20%", "Invested": "$20,000", "Current Value": "$20,000", "P/L ($)": "$0", "P/L (%)": "0.0%", "Role": "Healthcare"},
    {"Ticker": "SHV", "Allocation": "15%", "Invested": "$15,000", "Current Value": "$15,000", "P/L ($)": "$0", "P/L (%)": "0.0%", "Role": "Liquidity Buffer"}
]

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
        <tr><th>Ticker</th><th>Allocation</th><th>Invested</th><th>Current Value</th><th>P/L ($)</th><th>P/L (%)</th><th>Role</th></tr>
"""

for row in portfolio_data:
    html += f"<tr><td>{row['Ticker']}</td><td>{row['Allocation']}</td><td>{row['Invested']}</td><td>{row['Current Value']}</td><td>{row['P/L ($)']}</td><td>{row['P/L (%)']}</td><td>{row['Role']}</td></tr>"

html += "</table></body></html>"

with open('/home/warwick/.openclaw/workspace/CURRENT_PORTFOLIO.html', 'w') as f:
    f.write(html)
