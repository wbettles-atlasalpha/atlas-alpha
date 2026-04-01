import sys
sys.path.append('/home/warwick/.openclaw/workspace/scripts')
from data import get_news, get_bars

def check_drift(symbol):
    # Check news for catalyst
    news = get_news(symbol, days_back=7)
    # Check bars for 5% gap
    bars = get_bars(symbol, days=5)
    if not bars:
        return None
    
    last = bars[-1]
    prev = bars[-2]
    gap = (last['c'] - prev['c']) / prev['c'] * 100
    
    return {
        "symbol": symbol,
        "gap": gap,
        "catalyst_news": news[0]['headline'] if news else "No recent news found"
    }

print(check_drift("RIVN"))
print(check_drift("RKLB"))
print(check_drift("LUNR"))
