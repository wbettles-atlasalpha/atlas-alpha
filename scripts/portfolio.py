"""
Atlas Alpha - Portfolio Manager
Syncs PORTFOLIO_STATE.json and PORTFOLIO_LEDGER.csv with live Alpaca data.
"""

import json, csv, os
from datetime import datetime, date
from scripts.data import get_positions, get_account, get_news

WORKSPACE    = "/home/warwick/.openclaw/workspace"
STATE_FILE   = f"{WORKSPACE}/PORTFOLIO_STATE.json"
LEDGER_FILE  = f"{WORKSPACE}/PORTFOLIO_LEDGER.csv"
ASX_FILE     = f"{WORKSPACE}/ASX_PORTFOLIO.md"

# Hard-coded invalidation levels and metadata (source of truth)
POSITION_META = {
    "MOD":  {"invalidation": 175.0, "category": "Growth",   "conf": "90%", "date": "2026-03-17"},
    "ASTS": {"invalidation": 75.0,  "category": "Moonshot", "conf": "85%", "date": "2026-03-17"},
    "VKTX": {"invalidation": 30.0,  "category": "Moonshot", "conf": "85%", "date": "2026-03-17"},
}


def load_state() -> dict:
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def sync_from_alpaca() -> dict:
    """Pull live data from Alpaca, update state + ledger. Returns summary dict."""
    positions = get_positions()
    account   = get_account()

    portfolio_value = float(account["portfolio_value"])
    cash            = float(account["cash"])
    starting        = 100000.0

    rows    = []
    winners = []
    losers  = []
    alerts  = []
    total_pl = 0.0

    for p in positions:
        sym     = p["symbol"]
        qty     = float(p["qty"])
        entry   = float(p["avg_entry_price"])
        current = float(p["current_price"])
        pl      = float(p["unrealized_pl"])
        pl_pct  = float(p["unrealized_plpc"]) * 100
        meta    = POSITION_META.get(sym, {})
        inv     = meta.get("invalidation", 0)
        total_pl += pl

        if pl >= 0:
            winners.append(sym)
        else:
            losers.append(sym)

        # Invalidation gap alert (within 10%)
        if inv and current > 0:
            gap_pct = (current - inv) / current * 100
            if gap_pct < 10:
                alerts.append({
                    "symbol": sym, "current": current,
                    "invalidation": inv, "gap_pct": round(gap_pct, 1)
                })

        rows.append({
            "date":         meta.get("date", str(date.today())),
            "ticker":       sym,
            "action":       "BUY",
            "shares":       qty,
            "entry_usd":    round(entry, 2),
            "current_usd":  round(current, 2),
            "total_cost":   round(qty * entry, 2),
            "category":     meta.get("category", "Unknown"),
            "confidence":   meta.get("conf", "N/A"),
            "invalidation": inv,
            "pl_usd":       round(pl, 2),
            "pl_pct":       round(pl_pct, 2),
            "status":       "OPEN",
        })

    win_rate = round(len(winners) / len(positions) * 100, 1) if positions else 0.0

    # Save state
    state = {
        "starting_capital_usd":    starting,
        "current_cash_usd":        round(cash, 2),
        "equity_usd":              round(portfolio_value, 2),
        "total_value_usd":         round(portfolio_value, 2),
        "total_unrealized_pl_usd": round(total_pl, 2),
        "total_return_pct":        round((portfolio_value - starting) / starting * 100, 2),
        "open_positions":          [p["symbol"] for p in positions],
        "closed_trades":           0,
        "winning_trades":          len(winners),
        "losing_trades":           len(losers),
        "win_rate_pct":            win_rate,
        "last_updated":            datetime.utcnow().isoformat() + "Z",
    }
    save_state(state)

    # Save ledger
    fieldnames = ["date","ticker","action","shares","entry_usd","current_usd",
                  "total_cost","category","confidence","invalidation","pl_usd","pl_pct","status"]
    with open(LEDGER_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {
        "portfolio_value": portfolio_value,
        "total_pl":        total_pl,
        "total_return_pct": state["total_return_pct"],
        "win_rate":        win_rate,
        "winners":         winners,
        "losers":          losers,
        "alerts":          alerts,
        "positions":       rows,
    }


def check_invalidations(positions: list) -> list:
    """Return list of positions within 10% of their invalidation level."""
    alerts = []
    for p in positions:
        sym = p["ticker"]
        meta = POSITION_META.get(sym, {})
        inv = meta.get("invalidation", 0)
        current = p["current_usd"]
        if inv and current > 0:
            gap_pct = (current - inv) / current * 100
            if gap_pct < 10:
                alerts.append({
                    "symbol": sym, "current": current,
                    "invalidation": inv, "gap_pct": round(gap_pct, 1)
                })
    return alerts


if __name__ == "__main__":
    print("Syncing portfolio from Alpaca...")
    summary = sync_from_alpaca()
    print(f"Portfolio Value: ${summary['portfolio_value']:,.2f}")
    print(f"Total P/L:       ${summary['total_pl']:+,.2f} ({summary['total_return_pct']:+.2f}%)")
    print(f"Win Rate:        {summary['win_rate']}% ({len(summary['winners'])}/{len(summary['winners'])+len(summary['losers'])})")
    if summary["alerts"]:
        print(f"⚠️  Invalidation alerts: {summary['alerts']}")
