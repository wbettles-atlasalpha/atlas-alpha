import json

with open('/home/warwick/.openclaw/workspace/final_dynamic_results.json', 'r') as f:
    data = json.load(f)

# Analysis Logic
html = "<html><head><style>body{font-family:sans-serif;padding:40px;} table{width:100%;border-collapse:collapse;margin:20px 0;} th,td{border:1px solid #000;padding:8px;text-align:center;} th{background:#eee;}</style></head><body>"
html += "<h1>Atlas Alpha: Dynamic Performance Audit (2023-2025)</h1>"
html += "<p><em>Strategy: VCP Trigger + 2x ATR Trailing Stop-Loss + 5% Invalidation Thesis</em></p>"

total_capital = 10000
for sym, vectors in data.items():
    if not vectors: continue
    
    html += f"<h2>{sym} Performance</h2>"
    html += "<table><tr><th>Date</th><th>Status</th><th>Return</th><th>Balance</th></tr>"
    
    balance = total_capital
    for v in vectors:
        balance = balance * (1 + (v['return'] / 100))
        status = "Invalidated" if v['invalidated'] else "Success"
        html += f"<tr><td>{v['date']}</td><td>{status}</td><td>{v['return']}%</td><td>${balance:,.2f}</td></tr>"
    html += "</table>"
    html += f"<p><strong>Final Balance (from $10k):</strong> ${balance:,.2f}</p>"

html += "</body></html>"

with open('/home/warwick/.openclaw/workspace/PERFORMANCE_AUDIT_2025_DYNAMIC_FINAL.html', 'w') as f:
    f.write(html)
