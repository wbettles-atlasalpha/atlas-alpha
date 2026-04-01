"""
Atlas Alpha - Optimized Morning Automation
Single pipeline that sends exactly 3 messages to WhatsApp.
"""

import sys, json
sys.path.insert(0, "/home/warwick/.openclaw/workspace")

from scripts.portfolio   import sync_from_alpaca
from scripts.volume_scan import scan as volume_scan, format_picks
from scripts.macro_scan  import get_macro_snapshot, format_macro
from scripts.reddit_sniper import run as reddit_sniper, format_leads
from scripts.data        import get_quote_yf

def send_whatsapp(message: str):
    import subprocess
    subprocess.run(["openclaw", "message", "send", "--channel", "whatsapp", "--target", "+61481879871", "--message", message])

def run():
    # 1. Pipeline execution
    summary = sync_from_alpaca()
    picks = volume_scan(top_n=3)
    macro_snap = get_macro_snapshot()
    leads = reddit_sniper(top_n=3)

    # 2. Newsletter (Message 1)
    newsletter = f"📰 *ATLAS ALPHA DAILY MARKET INSIGHTS*\n\n{format_macro(macro_snap)}\n\nStay ahead of the drift."
    send_whatsapp(newsletter)

    # 3. Master Strategy Vectors (Message 2)
    vectors = f"🎯 *MASTER STRATEGY VECTORS*\n\n{format_picks(picks, title='Top Setups')}\n\n*Invalidation Thesis:* If price breaches 5% from entry, vector is voided."
    send_whatsapp(vectors)

    # 4. Portfolio Update (Message 3)
    port = f"💼 *PAPER PORTFOLIO UPDATE*\n\nValue: ${summary['portfolio_value']:,.2f}\nAction: {'Holding position' if summary['win_rate'] > 40 else 'Reviewing all stop-losses'}"
    send_whatsapp(port)

if __name__ == "__main__":
    run()
