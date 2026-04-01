import json

with open('/home/warwick/.openclaw/workspace/alpha_vectors_final.json', 'r') as f:
    data = json.load(f)

html = """
<html>
<head>
    <style>
        body { font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 40px; }
        h1 { border-bottom: 2px solid #1a2a6c; color: #1a2a6c; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>Atlas Alpha: Alpha Vector Report</h1>
    <p>This list is ranked by total Alpha Score (Fundamental Health + Institutional Footprint). Scores > 10 indicate high-conviction targets.</p>
    <table>
        <tr><th>Ticker</th><th>Fundamental Score</th><th>Technical Score</th><th>Total Alpha Score</th></tr>
"""

for item in data:
    html += f"<tr><td>{item['ticker']}</td><td>{item['fundamental_score']}</td><td>{item['technical_score']}</td><td>{item['total_alpha_score']}</td></tr>"

html += "</table></body></html>"

with open('/home/warwick/.openclaw/workspace/ALPHA_VECTOR_REPORT.html', 'w') as f:
    f.write(html)
