import json

with open('/home/warwick/.openclaw/workspace/SP500_10Y_RESULTS.json', 'r') as f:
    data = json.load(f)

html = """
<html>
<head>
    <style>
        body { font-family: 'Helvetica', sans-serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 40px; }
        h1 { border-bottom: 3px solid #1a2a6c; color: #1a2a6c; }
        .summary-box { background: #f0f7ff; padding: 20px; border-left: 5px solid #1a2a6c; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #000; padding: 10px; text-align: center; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>Atlas Alpha: 10-Year Backtest (2016-2025)</h1>
    <div class="summary-box">
        <h3>Applied Constraints</h3>
        <ul>
            <li><strong>Trend:</strong> Price > 200-day SMA</li>
            <li><strong>Exclusion 1:</strong> RSI < 65</li>
            <li><strong>Exclusion 2:</strong> SMA50 Stretch < 8%</li>
            <li><strong>Institutional Parity:</strong> Volume Ratio 0.9-1.1, ATR Stability 2-4%</li>
        </ul>
    </div>
"""

total_vectors = 0
total_return = 0

for sym, vectors in data.items():
    if not vectors: continue
    html += f"<h2>{sym}</h2><table><tr><th>Date</th><th>Return</th></tr>"
    for v in vectors:
        total_vectors += 1
        total_return += v['return']
        html += f"<tr><td>{v['date']}</td><td>{v['return']}%</td></tr>"
    html += "</table>"

if total_vectors > 0:
    html += f"<h2>Summary</h2><p>Total Vectors: {total_vectors}</p><p>Avg Return: {round(total_return/total_vectors, 2)}%</p>"

html += "</body></html>"

with open('/home/warwick/.openclaw/workspace/FINAL_10Y_AUDIT.html', 'w') as f:
    f.write(html)
