import json

# Defensive positions with Entry Prices (Market Open, Monday Night) and Live Prices
# Entry prices assume Monday night market open values: XLE: 62.76, XLP: 81.87, XLV: 142.90, SHV: 110.37
data = {
    "XLE": {"alloc": "35%", "invested": 35000, "entry": 62.76, "live": 61.96},
    "XLP": {"alloc": "30%", "invested": 30000, "entry": 81.87, "live": 81.88},
    "XLV": {"alloc": "20%", "invested": 20000, "entry": 142.90, "live": 143.82},
    "SHV": {"alloc": "15%", "invested": 15000, "entry": 110.37, "live": 110.38}
}

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
        <tr><th>Ticker</th><th>Allocation</th><th>Invested</th><th>Entry Price</th><th>Live Price</th><th>P/L ($)</th><th>P/L (%)</th></tr>
"""

for ticker, info in data.items():
    current_val = info["invested"] * (info["live"] / info["entry"])
    pl_usd = current_val - info["invested"]
    pl_pct = (info["live"] - info["entry"]) / info["entry"] * 100
    html += f"<tr><td>{ticker}</td><td>{info['alloc']}</td><td>${info['invested']:,.2f}</td><td>${info['entry']:.2f}</td><td>${info['live']:.2f}</td><td>${pl_usd:,.2f}</td><td>{pl_pct:.2f}%</td></tr>"

html += "</table></body></html>"

with open('/home/warwick/.openclaw/workspace/CURRENT_PORTFOLIO.html', 'w') as f:
    f.write(html)
