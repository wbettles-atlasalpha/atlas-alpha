"""
Atlas Alpha - Morning Brief Orchestrator
Runs the full daily pipeline and sends a structured WhatsApp brief.
Designed to run as an isolated cron sub-agent to avoid burning main session tokens.

Pipeline:
  1. Sync portfolio from Alpaca
  2. Volume scan for new US setups
  3. Macro environment check
  4. ASX shadow portfolio update (yfinance)
  5. Reddit Sniper leads
  6. Compose + send WhatsApp brief in sections
"""

import sys, os, json
sys.path.insert(0, "/home/warwick/.openclaw/workspace")

import urllib.request, urllib.parse

from scripts.portfolio   import sync_from_alpaca
from scripts.volume_scan import scan as volume_scan, format_picks
from scripts.macro_scan  import get_macro_snapshot, format_macro, yield_curve_signal
from scripts.reddit_sniper import run as reddit_sniper, format_leads
from scripts.data        import get_quote_yf

# ── Config ────────────────────────────────────────────────────────────────────
WHATSAPP_NUMBER = "+61481879871"
OPENCLAW_TOKEN  = "b982a778ce052ef020d7150006984d408c7aa26933d0f3c4"
OPENCLAW_PORT   = 18789

ASX_HOLDINGS = {}


def send_whatsapp(message: str):
    """Send a message to Warwick's WhatsApp via OpenClaw CLI."""
    import subprocess
    try:
        result = subprocess.run(
            [
                "openclaw", "message", "send",
                "--channel", "whatsapp",
                "--target", WHATSAPP_NUMBER,
                "--message", message,
                "--json",
            ],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print(f"WhatsApp send error (rc={result.returncode}): {result.stderr.strip()}", file=sys.stderr)
            return None
        return json.loads(result.stdout) if result.stdout.strip() else {"ok": True}
    except Exception as e:
        print(f"WhatsApp send error: {e}", file=sys.stderr)
        return None


def build_portfolio_section(summary: dict) -> str:
    total_return = summary["total_return_pct"]
    arrow = "📈" if total_return >= 0 else "📉"
    sign  = "+" if total_return >= 0 else ""

    lines = [
        f"📊 *PORTFOLIO* — {arrow} {sign}{total_return:.2f}%",
        f"Value: ${summary['portfolio_value']:,.2f} | P/L: ${summary['total_pl']:+,.2f}",
        f"Win Rate: {summary['win_rate']}% ({len(summary['winners'])}/{len(summary['winners'])+len(summary['losers'])} positions)",
    ]

    if summary["winners"]:
        lines.append(f"✅ Green: {', '.join(summary['winners'])}")
    if summary["losers"]:
        lines.append(f"🔴 Red:   {', '.join(summary['losers'])}")

    if summary["alerts"]:
        lines.append("\n⚠️ *INVALIDATION WATCH:*")
        for a in summary["alerts"]:
            lines.append(f"  • {a['symbol']} ${a['current']:.2f} → inv ${a['invalidation']:.2f} (gap {a['gap_pct']:.1f}%)")

    return "\n".join(lines)


def build_asx_section() -> str:
    lines = ["🇦🇺 *ASX SHADOW PORTFOLIO*"]
    for ticker, info in ASX_HOLDINGS.items():
        q = get_quote_yf(ticker)
        if q and q.get("price") and not q.get("error"):
            price  = q["price"]
            pl     = (price - info["entry"]) * info["qty"]
            pl_pct = (price - info["entry"]) / info["entry"] * 100
            arrow  = "📈" if pl >= 0 else "📉"
            lines.append(f"{arrow} *{ticker}* ({info['name']}) ${price:.2f} AUD | P/L ${pl:+.0f} ({pl_pct:+.1f}%)")
        else:
            lines.append(f"⚪ *{ticker}* ({info['name']}) — price unavailable (market closed?)")
    return "\n".join(lines)


def run():
    print("=== Atlas Alpha Morning Brief ===")

    # 1. Portfolio sync
    print("Syncing portfolio...")
    try:
        summary = sync_from_alpaca()
    except Exception as e:
        summary = None
        print(f"Portfolio sync error: {e}", file=sys.stderr)

    # 2. Volume scan
    print("Running volume scan...")
    try:
        picks = volume_scan(top_n=5)
        us_section = format_picks(picks, title="🇺🇸 US PICKS OF THE DAY")
    except Exception as e:
        us_section = f"🇺🇸 *US PICKS* — scan error: {e}"
        picks = []

    # 3. Macro
    print("Checking macro...")
    try:
        macro_snap = get_macro_snapshot()
        macro_section = format_macro(macro_snap)
    except Exception as e:
        macro_section = f"*Macro* — unavailable: {e}"

    # 4. ASX
    print("Checking ASX...")
    asx_section = build_asx_section()

    # 5. Reddit Sniper
    print("Running Reddit Sniper...")
    try:
        leads = reddit_sniper(top_n=5)
        reddit_section = format_leads(leads)
    except Exception as e:
        reddit_section = f"*Reddit Sniper* — error: {e}"

    # ── Send in sections (avoids hitting message length limits) ──────────────

    # Section 1: Header + Portfolio
    header = "🌐 *ATLAS ALPHA — DAILY BRIEF*\n━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if summary:
        portfolio_section = build_portfolio_section(summary)
    else:
        portfolio_section = "📊 *PORTFOLIO* — sync failed, check Alpaca connection"

    send_whatsapp(f"{header}\n\n{portfolio_section}")

    # Section 2: Macro + US Picks
    send_whatsapp(f"{macro_section}\n\n{us_section}")

    # Section 3: ASX
    send_whatsapp(asx_section)

    # Section 4: Reddit Sniper
    send_whatsapp(reddit_section)

    # Section 5: Verdict
    verdict = build_verdict(summary, picks, macro_snap if 'macro_snap' in dir() else {})
    send_whatsapp(verdict)

    print("Brief delivered.")


def build_verdict(summary, picks, macro_snap) -> str:
    lines = ["🏁 *ATLAS VERDICT*"]

    if summary:
        if summary["total_return_pct"] < -5:
            lines.append("Portfolio under pressure — review invalidation levels before adding risk.")
        elif summary["alerts"]:
            symbols = [a["symbol"] for a in summary["alerts"]]
            lines.append(f"Watch {', '.join(symbols)} closely — approaching invalidation. Cut if breached, no exceptions.")
        else:
            lines.append("Portfolio healthy — all positions above invalidation levels.")

    if picks:
        top = picks[0]
        lines.append(f"Top setup: *{top['symbol']}* {top['chg_pct']:+.2f}% on {top['vol_ratio']:.1f}x volume — worth a deeper look.")
    else:
        lines.append("No high-conviction volume setups today. Patience is a position.")

    lines.append("\n— Atlas 🌐")
    return "\n".join(lines)


if __name__ == "__main__":
    run()
