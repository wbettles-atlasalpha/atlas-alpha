"""
Atlas Alpha - Volume Spike Scanner
Scans a broad watchlist for volume anomalies (>1.5x avg) and price momentum.
Uses Alpaca batch bars + yfinance fallback. No Alpha Vantage.
"""

import sys
from data import get_multi_bars, volume_ratio, get_news

# ── Watchlist ─────────────────────────────────────────────────────────────────
# Curated universe: high-beta momentum names worth watching for Atlas Alpha
WATCHLIST = [
    # AI / Semis
    "NVDA","AMD","ARM","AVGO","MRVL","SMCI","TSM","INTC",
    # Cloud / SaaS
    "SNOW","DDOG","NET","ZS","OKTA","CRWD","FTNT",
    # Growth / Disruptive
    "PLTR","SHOP","ABNB","UBER","LYFT","RBLX","U",
    # Space / Defence
    "RKLB","LUNR","ASTS","HII","RTX",
    # Fintech
    "HOOD","COIN","SQ","AFRM","UPST","PYPL",
    # Biotech / Health
    "HIMS","RXRX","MRNA","NVAX","XENE",
    # EV / Energy
    "TSLA","RIVN","LCID","PLUG","FCEL",
    # Consumer / Retail
    "APP","TTWO","EA","NFLX","DIS",
    # Value / Macro plays
    "META","AMZN","ORCL","MSFT","GOOGL",
]

SPIKE_THRESHOLD = 1.5  # volume ratio to flag as significant


def scan(watchlist: list = None, threshold: float = SPIKE_THRESHOLD, top_n: int = 10) -> list:
    """
    Scan watchlist for volume spikes. Returns top_n results sorted by vol ratio.
    Each result: {symbol, close, chg_pct, vol_ratio, high, low, news}
    """
    symbols = watchlist or WATCHLIST
    results = []

    # Batch fetch in chunks of 20 (Alpaca limit per request)
    chunk_size = 20
    all_bars = {}
    for i in range(0, len(symbols), chunk_size):
        chunk = symbols[i:i+chunk_size]
        try:
            bars = get_multi_bars(chunk, days=10)
            all_bars.update(bars)
        except Exception as e:
            print(f"Batch fetch error (chunk {i}): {e}", file=sys.stderr)

    for sym, bars in all_bars.items():
        if not bars or len(bars) < 2:
            continue
        last   = bars[-1]
        prev   = bars[-2]
        vr     = volume_ratio(bars)
        chg    = (last["c"] - prev["c"]) / prev["c"] * 100 if prev["c"] else 0

        results.append({
            "symbol":    sym,
            "close":     round(last["c"], 2),
            "chg_pct":   round(chg, 2),
            "vol_ratio": vr,
            "high":      round(last["h"], 2),
            "low":       round(last["l"], 2),
        })

    # Sort by vol ratio descending, filter above threshold
    spikes = [r for r in results if r["vol_ratio"] >= threshold]
    spikes.sort(key=lambda x: x["vol_ratio"], reverse=True)
    top = spikes[:top_n]

    # Enrich top picks with news
    for pick in top[:5]:
        pick["news"] = get_news(pick["symbol"], days_back=2)

    return top


def format_picks(picks: list, title: str = "US Volume Spikes") -> str:
    """Format picks as a WhatsApp-friendly string."""
    if not picks:
        return f"*{title}*\nNo significant volume spikes detected today."

    lines = [f"*{title}*"]
    for p in picks:
        arrow  = "📈" if p["chg_pct"] >= 0 else "📉"
        line   = f"{arrow} *{p['symbol']}* ${p['close']:.2f} ({p['chg_pct']:+.2f}%) | Vol {p['vol_ratio']:.1f}x"
        lines.append(line)
        if p.get("news"):
            headline = p["news"][0]["headline"][:80]
            lines.append(f"  ↳ _{headline}_")
    return "\n".join(lines)


if __name__ == "__main__":
    print("Running volume scan...")
    picks = scan()
    print(format_picks(picks))
