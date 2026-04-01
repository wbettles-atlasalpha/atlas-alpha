import json
from datetime import datetime

with open('/home/warwick/.openclaw/workspace/SP500_10Y_RESULTS.json', 'r') as f:
    data = json.load(f)

# Initialize stats
stats = {}

for symbol, vectors in data.items():
    for v in vectors:
        year = datetime.strptime(v['date'], '%Y-%m-%d').year
        if year not in stats:
            stats[year] = {"total": 0, "wins": 0, "total_return": 0}
        
        stats[year]["total"] += 1
        stats[year]["total_return"] += v['return']
        if v['return'] > 0:
            stats[year]["wins"] += 1

print(f"{'Year':<6} | {'Vectors':<8} | {'Success':<8} | {'Avg Return':<12}")
print("-" * 45)
for year in sorted(stats.keys()):
    s = stats[year]
    win_rate = (s['wins'] / s['total']) * 100
    avg_ret = s['total_return'] / s['total']
    print(f"{year:<6} | {s['total']:<8} | {win_rate:<7.1f}% | {avg_ret:<11.2f}%")
