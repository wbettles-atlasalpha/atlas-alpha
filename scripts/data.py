"""
Atlas Alpha - Unified Data Module
Primary:  Alpaca Markets API (US equities)
Fallback: yfinance (US + ASX)
Retired:  Alpha Vantage (rate limit: 25/day - too low for production use)
"""

import urllib.request, json, time
from datetime import datetime, timedelta, date

# ── Credentials ──────────────────────────────────────────────────────────────
ALPACA_KEY    = "PKLXTM37LF7Y4PUXRKAUAJEWC5"
ALPACA_SECRET = "Evk5W9HHZc9ZmB8jbqKE52KGE6SNWoy5hXSrLHvCaDCq"
ALPACA_TRADE  = "https://paper-api.alpaca.markets"
ALPACA_DATA   = "https://data.alpaca.markets"
FINNHUB_KEY   = "d6n9cvhr01qlnj39nfm0d6n9cvhr01qlnj39nfmg"


# ── Alpaca helpers ────────────────────────────────────────────────────────────
def _alpaca_get(path, base=ALPACA_DATA):
    req = urllib.request.Request(
        f"{base}{path}",
        headers={"APCA-API-KEY-ID": ALPACA_KEY, "APCA-API-SECRET-KEY": ALPACA_SECRET}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def get_positions():
    """Return all open Alpaca paper positions as a list of dicts."""
    return _alpaca_get("/v2/positions", base=ALPACA_TRADE)


def get_account():
    """Return Alpaca account summary."""
    return _alpaca_get("/v2/account", base=ALPACA_TRADE)


def get_bars(symbol: str, days: int = 5, feed: str = "iex") -> list:
    """Return daily OHLCV bars for a US symbol. Returns list oldest→newest."""
    end   = date.today().strftime("%Y-%m-%d")
    start = (date.today() - timedelta(days=days + 5)).strftime("%Y-%m-%d")  # buffer for weekends
    data  = _alpaca_get(f"/v2/stocks/{symbol}/bars?timeframe=1Day&start={start}&end={end}&feed={feed}")
    return data.get("bars") or []


def get_multi_bars(symbols: list, days: int = 5, feed: str = "iex") -> dict:
    """Batch fetch bars for multiple symbols in one request. Returns {symbol: [bars]}."""
    end   = date.today().strftime("%Y-%m-%d")
    start = (date.today() - timedelta(days=days + 5)).strftime("%Y-%m-%d")
    syms  = "%2C".join(symbols)
    data  = _alpaca_get(f"/v2/stocks/bars?symbols={syms}&timeframe=1Day&start={start}&end={end}&feed={feed}")
    return data.get("bars") or {}


def get_quote_alpaca(symbol: str) -> dict | None:
    """Latest trade quote for a single US symbol via Alpaca."""
    try:
        data = _alpaca_get(f"/v2/stocks/{symbol}/quotes/latest?feed=iex")
        q = data.get("quote", {})
        return {"symbol": symbol, "ask": q.get("ap", 0), "bid": q.get("bp", 0)}
    except Exception:
        return None


# ── yfinance helpers (US + ASX fallback) ─────────────────────────────────────
def get_quote_yf(symbol: str) -> dict | None:
    """Get quote via yfinance. Works for US and ASX (e.g. 'JBH.AX')."""
    try:
        import yfinance as yf
        t = yf.Ticker(symbol)
        info = t.fast_info
        price = info.get("lastPrice") or info.get("regularMarketPrice") or 0
        prev  = info.get("previousClose") or price
        chg_pct = ((price - prev) / prev * 100) if prev else 0
        return {
            "symbol":   symbol,
            "price":    round(price, 4),
            "prev":     round(prev, 4),
            "chg_pct":  round(chg_pct, 2),
            "volume":   info.get("lastVolume") or 0,
            "mktcap":   info.get("marketCap") or 0,
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def get_multi_quotes_yf(symbols: list) -> dict:
    """Batch yfinance quotes. Returns {symbol: quote_dict}."""
    try:
        import yfinance as yf
        tickers = yf.Tickers(" ".join(symbols))
        results = {}
        for sym in symbols:
            try:
                t    = tickers.tickers[sym]
                info = t.fast_info
                price = info.get("lastPrice") or info.get("regularMarketPrice") or 0
                prev  = info.get("previousClose") or price
                chg   = ((price - prev) / prev * 100) if prev else 0
                results[sym] = {
                    "symbol":  sym,
                    "price":   round(price, 4),
                    "prev":    round(prev, 4),
                    "chg_pct": round(chg, 2),
                    "volume":  info.get("lastVolume") or 0,
                }
            except Exception as e:
                results[sym] = {"symbol": sym, "error": str(e)}
        return results
    except Exception as e:
        return {s: {"symbol": s, "error": str(e)} for s in symbols}


# ── Finnhub news ──────────────────────────────────────────────────────────────
def get_news(symbol: str, days_back: int = 2) -> list:
    """Return recent company news headlines from Finnhub."""
    try:
        frm = (date.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        to  = date.today().strftime("%Y-%m-%d")
        url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={frm}&to={to}&token={FINNHUB_KEY}"
        with urllib.request.urlopen(url, timeout=10) as r:
            items = json.loads(r.read())
        return [{"headline": n.get("headline", ""), "source": n.get("source", ""), "url": n.get("url", "")}
                for n in items[:5]]
    except Exception:
        return []


def get_market_news(category: str = "general", limit: int = 10) -> list:
    """Return broad market news from Finnhub."""
    try:
        url = f"https://finnhub.io/api/v1/news?category={category}&token={FINNHUB_KEY}"
        with urllib.request.urlopen(url, timeout=10) as r:
            items = json.loads(r.read())
        return [{"headline": n.get("headline", ""), "source": n.get("source", "")}
                for n in items[:limit]]
    except Exception:
        return []


# ── Convenience: volume spike score ──────────────────────────────────────────
def volume_ratio(bars: list) -> float:
    """Compare latest bar volume vs average of prior bars."""
    if len(bars) < 2:
        return 0.0
    prev_vols = [b["v"] for b in bars[:-1] if b.get("v", 0) > 0]
    if not prev_vols:
        return 0.0
    avg = sum(prev_vols) / len(prev_vols)
    return round(bars[-1]["v"] / avg, 2) if avg else 0.0


if __name__ == "__main__":
    print("Testing data module...")
    pos = get_positions()
    print(f"Open positions: {[p['symbol'] for p in pos]}")
    acct = get_account()
    print(f"Portfolio value: ${float(acct['portfolio_value']):,.2f}")
    q = get_quote_yf("JBH.AX")
    print(f"JBH.AX (yfinance): {q}")
