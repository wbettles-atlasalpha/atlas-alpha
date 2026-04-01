import json

with open('/home/warwick/.openclaw/workspace/precision_audit_results.json', 'r') as f:
    data = json.load(f)

html = "<html><head><style>body{font-family:sans-serif;padding:40px;} table{width:100%;border-collapse:collapse;} th,td{border:1px solid #000;padding:8px;} th{background:#eee;}</style></head><body>"
html += "<h1>Precision Alpha: 75% Success Target Audit</h1>"

total_wins = 0
total_vectors = 0

for sym, vectors in data.items():
    if not vectors: continue
    html += f"<h2>{sym}</h2><table><tr><th>Date</th><th>Invalidated</th><th>Return</th></tr>"
    for v in vectors:
        total_vectors += 1
        if not v['invalidated']: total_wins += 1
        status = "Invalidated" if v['invalidated'] else "Success"
        html += f"<tr><td>{v['date']}</td><td>{status}</td><td>{v['return']}%</td></tr>"
    html += "</table>"

if total_vectors > 0:
    success_rate = (total_wins / total_vectors) * 100
    html += f"<h2>Audit Summary</h2><p><strong>Success Rate:</strong> {round(success_rate, 2)}%</p>"
    html += f"<p><strong>Total Vectors Identified:</strong> {total_vectors}</p>"

html += "</body></html>"

with open('/home/warwick/.openclaw/workspace/PRECISION_AUDIT_REPORT.html', 'w') as f:
    f.write(html)
