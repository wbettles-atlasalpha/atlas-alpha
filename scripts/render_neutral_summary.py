import json

# Load the raw results from the last audit
with open('/home/warwick/.openclaw/workspace/MARKET_NEUTRAL_RESULTS.json', 'r') as f:
    data = json.load(f)

# Metrics: Totals, Win Rate, Avg Return
stats = {"LONG": {"wins": 0, "total": 0, "ret": 0}, "SHORT": {"wins": 0, "total": 0, "ret": 0}}

for v in data:
    side = v['side']
    stats[side]["total"] += 1
    stats[side]["ret"] += v['return']
    if v['return'] > 0:
        stats[side]["wins"] += 1

html = """
<html>
<head>
    <style>
        body { font-family: sans-serif; padding: 40px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #000; padding: 10px; text-align: center; }
        th { background: #eee; }
        .summary { background: #e0f7fa; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Market Neutral Strategy Performance (2023-2025)</h1>
    <div class="summary">
        <h2>Aggregated Performance</h2>
        <table>
            <tr><th>Side</th><th>Total Vectors</th><th>Success Rate</th><th>Avg. Return</th></tr>
"""

for side, s in stats.items():
    win_rate = (s['wins'] / s['total']) * 100 if s['total'] > 0 else 0
    avg_ret = s['ret'] / s['total'] if s['total'] > 0 else 0
    html += f"<tr><td>{side}</td><td>{s['total']}</td><td>{win_rate:.2f}%</td><td>{avg_ret:.2f}%</td></tr>"

html += "</table></div></body></html>"

with open('/home/warwick/.openclaw/workspace/MARKET_NEUTRAL_SUMMARY.html', 'w') as f:
    f.write(html)
