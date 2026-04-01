import json

# Internal Audit Data: Performance Tracking for Recent Rotations
audit_history = [
    {"date": "2026-03-30", "rotation": "BEAR-LIQUIDITY", "conf": 8.5, "outcome": "Stable (Hedged)", "pl_pct": -0.31},
    {"date": "2026-03-24", "rotation": "DRIFT-ROTATION", "conf": 7.8, "outcome": "Liquidated (Loss)", "pl_pct": -2.45},
    {"date": "2026-03-17", "rotation": "GROWTH-VCP", "conf": 8.2, "outcome": "Positive", "pl_pct": 1.12}
]

portfolio_data = {
    "XLE": {"alloc": "35%", "invested": 35000, "entry": 62.76, "live": 61.96, "role": "Energy Hedge", "inv": 58.00},
    "XLP": {"alloc": "30%", "invested": 30000, "entry": 81.87, "live": 81.88, "role": "Consumer Staples", "inv": 78.00},
    "XLV": {"alloc": "20%", "invested": 20000, "entry": 142.90, "live": 143.82, "role": "Healthcare", "inv": 135.00},
    "SHV": {"alloc": "15%", "invested": 15000, "entry": 110.37, "live": 110.38, "role": "Liquidity Buffer", "inv": 109.50}
}

html = """
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
        body { font-family: 'Space Grotesk', sans-serif; background: #0b0e14; padding: 20px; color: #e0e0e0; }
        .card { background: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; max-width: 800px; margin: 0 auto 20px; }
        h1, h2 { color: #58a6ff; margin-top: 0; font-size: 1.2rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem; }
        th { background: #21262d; color: #8b949e; padding: 8px; border-bottom: 2px solid #30363d; text-transform: uppercase; letter-spacing: 1px; font-size: 0.75rem; }
        td { border-bottom: 1px solid #30363d; padding: 8px; text-align: center; font-weight: 500; }
        .pos { color: #3fb950; } .neg { color: #f85149; }
        .alert { color: #d29922; }
        tr:hover { background: #1c2128; }
        .chart-container { max-width: 400px; margin: 0 auto; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1 style="text-align: center;">🌐 ATLAS ALPHA | PORTFOLIO INTEL</h1>
    
    <div class="card">
        <h2>DEFENSIVE ROTATION | ACTIVE</h2>
        <div class="chart-container"><canvas id="portfolioChart"></canvas></div>
        <table>
            <tr><th>Ticker</th><th>Role</th><th>Invested</th><th>Entry</th><th>Live</th><th>P/L ($)</th><th>Inv. Level</th></tr>
"""

total_pl_usd = 0
for ticker, info in portfolio_data.items():
    current_val = info["invested"] * (info["live"] / info["entry"])
    pl_usd = current_val - info["invested"]
    c = "pos" if pl_usd >= 0 else "neg"
    inv_class = "alert" if info["live"] < (info["inv"] * 1.05) else ""
    html += f"<tr><td><strong>{ticker}</strong></td><td>{info['role']}</td><td>${info['invested']:,.2f}</td><td>${info['entry']:.2f}</td><td>${info['live']:.2f}</td><td class='{c}'>${pl_usd:,.2f}</td><td class='{inv_class}'>${info['inv']:.2f}</td></tr>"

html += "</table></div>"

html += """
    <div class="card">
        <h2>MARKET OBSERVABILITY | LIQUIDITY PULSE</h2>
        <p style="font-size: 0.9rem; color: #8b949e;">Macro Liquidity Indicator: <strong>STABLE (NEUTRAL)</strong></p>
    </div>

    <div class="card">
        <h2>ENGINE PERFORMANCE AUDIT</h2>
        <div class="chart-container"><canvas id="auditChart"></canvas></div>
        <table>
            <tr><th>Date</th><th>Rotation</th><th>Engine Confidence</th><th>Outcome</th><th>P/L (%)</th></tr>
"""
for audit in audit_history:
    c = "pos" if audit['pl_pct'] >= 0 else "neg"
    html += f"<tr><td>{audit['date']}</td><td>{audit['rotation']}</td><td>{audit['conf']}</td><td>{audit['outcome']}</td><td class='{c}'>{audit['pl_pct']:.2f}%</td></tr>"

html += "</table></div>"

html += """
        <script>
            const ctx = document.getElementById('portfolioChart').getContext('2d');
            new Chart(ctx, { type: 'doughnut', data: { labels: [""" + ", ".join([f"'{t}'" for t in portfolio_data.keys()]) + """], datasets: [{ data: [""" + ", ".join([str(int(info['alloc'].replace('%',''))) for info in portfolio_data.values()]) + """], backgroundColor: ['#58a6ff', '#3fb950', '#d29922', '#f85149'] }] }, options: { plugins: { legend: { position: 'bottom', labels: { color: '#e0e0e0', boxWidth: 10 } } } } });
            const ctxA = document.getElementById('auditChart').getContext('2d');
            new Chart(ctxA, { type: 'line', data: { labels: [""" + ", ".join([f"'{a['date']}'" for a in audit_history[::-1]]) + """], datasets: [{ label: 'Engine Confidence', data: [""" + ", ".join([str(a['conf']) for a in audit_history[::-1]]) + """], borderColor: '#58a6ff', tension: 0.1 }] }, options: { scales: { y: { ticks: { color: '#e0e0e0' } }, x: { ticks: { color: '#e0e0e0' } } } } });
        </script>
</body></html>
"""

with open('/home/warwick/.openclaw/workspace/scripts/portfolio_performance.html', 'w') as f:
    f.write(html)
