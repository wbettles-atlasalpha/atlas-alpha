import json

with open('/home/warwick/.openclaw/workspace/MARKET_WIDE_AUDIT_LOG.json', 'r') as f:
    data = json.load(f)

html = "<html><head><style>body{font-family:sans-serif;padding:40px;} table{width:100%;border-collapse:collapse;} th,td{border:1px solid #000;padding:8px;} th{background:#eee;}</style></head><body>"
html += "<h1>Full Market Audit: 2023-2025</h1>"

for universe, vectors in data.items():
    html += f"<h2>{universe} ({len(vectors)} vectors found)</h2>"
    html += "<table><tr><th>Symbol</th><th>Date</th><th>Status</th><th>Return</th></tr>"
    for v in vectors:
        status = "Invalidated" if v['invalidated'] else "Success"
        # Removed entry because key was missing, will debug later if needed
        html += f"<tr><td>{v['symbol']}</td><td>{v['date']}</td><td>{status}</td><td>{v['return']}%</td></tr>"
    html += "</table>"

html += "</body></html>"

with open('/home/warwick/.openclaw/workspace/FULL_MARKET_AUDIT_LOG.html', 'w') as f:
    f.write(html)
