import json

with open('/home/warwick/.openclaw/workspace/audit_results_2025.json', 'r') as f:
    data = json.load(f)

html = "<html><head><style>body { font-family: sans-serif; padding: 40px; } table { width: 100%; border-collapse: collapse; margin-bottom: 40px; } th, td { border: 1px solid #000; padding: 8px; text-align: left; } th { background: #eee; }</style></head><body>"
html += "<h1>Full Performance Audit 2025</h1>"

for index, vectors in data.items():
    html += f"<h2>{index}</h2>"
    html += "<table><tr><th>Symbol</th><th>Date</th><th>Entry</th><th>Invalidated</th><th>Days</th><th>Return</th></tr>"
    for v in vectors:
        html += f"<tr><td>{v['symbol']}</td><td>{v['date']}</td><td>{v['entry']}</td><td>{v['invalidated']}</td><td>{v['days_held']}</td><td>{v['return']}%</td></tr>"
    html += "</table>"

html += "</body></html>"

with open('/home/warwick/.openclaw/workspace/PERFORMANCE_AUDIT_2025_FULL_DISCLOSURE.html', 'w') as f:
    f.write(html)
