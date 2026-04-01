import json

with open('/home/warwick/.openclaw/workspace/market_wide_results.json', 'r') as f:
    data = json.load(f)

html = "<html><head><style>body{font-family:sans-serif;padding:40px;} table{width:100%;border-collapse:collapse;margin:20px 0;} th,td{border:1px solid #000;padding:8px;} th{background:#eee;}</style></head><body>"
html += "<h1>Market-Wide Audit: Full Disclosure</h1>"

for universe, vectors in data.items():
    html += f"<h2>{universe} ({len(vectors)} vectors)</h2>"
    html += "<table><tr><th>Symbol</th><th>Date</th><th>Entry</th><th>Return</th></tr>"
    for v in vectors:
        html += f"<tr><td>{v['symbol']}</td><td>{v['date']}</td><td>{v['entry']}</td><td>{v['return']}%</td></tr>"
    html += "</table>"
    if vectors:
        avg_ret = sum(v['return'] for v in vectors) / len(vectors)
        html += f"<p><strong>Average Vector Return:</strong> {round(avg_ret, 2)}%</p>"

html += "</body></html>"

with open('/home/warwick/.openclaw/workspace/FULL_MARKET_AUDIT.html', 'w') as f:
    f.write(html)
