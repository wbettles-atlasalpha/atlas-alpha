import json

with open('/home/warwick/.openclaw/workspace/final_backtest_2023_2025.json', 'r') as f:
    data = json.load(f)

html = """
<html>
<head>
    <style>
        body { font-family: 'Helvetica', sans-serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 40px; }
        h1 { border-bottom: 3px solid #000; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #000; padding: 10px; text-align: center; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>Atlas Alpha: 3-Year Alpha Vector Audit (2023-2025)</h1>
    <p>This report documents the performance of the VCP "Institutional Footprint" engine across a 36-month backtest (2023-2025).</p>
"""

total_vectors = 0
total_returns = 0

for symbol, vectors in data.items():
    html += f"<h2>{symbol} Audit Log</h2>"
    html += "<table><tr><th>Date</th><th>Invalidated</th><th>Return</th></tr>"
    for v in vectors:
        total_vectors += 1
        total_returns += v['return']
        status = "Invalidated" if v['invalidated'] else "Success"
        html += f"<tr><td>{v['date']}</td><td>{status}</td><td>{v['return']}%</td></tr>"
    html += "</table>"

html += f"""
    <h2>Audit Summary</h2>
    <p>Total Vectors Identified: <strong>{total_vectors}</strong></p>
    <p>Average Vector Return: <strong>{round(total_returns/total_vectors, 2)}%</strong></p>
</body>
</html>
"""

with open('/home/warwick/.openclaw/workspace/FINAL_ALPHA_REPORT_2023_2025.html', 'w') as f:
    f.write(html)
