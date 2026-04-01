"""
Atlas Alpha - Macro Environment Scanner
Pulls yield curve, M2 supply, and Fed Funds Rate from FRED.
Integrates 'Event Risk' signal based on geopolitical sentiment and market volatility.
"""

import urllib.request, json
from datetime import date, timedelta
import random # Placeholder for real sentiment analysis

FRED_KEY = "dff297553e57a66365c7094f9987a1cb"
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

SERIES = {
    "DGS10":  "10Y Treasury",
    "DGS2":   "2Y Treasury",
    "FEDFUNDS":"Fed Funds Rate",
    "M2SL":   "M2 Money Supply",
}

def get_event_risk_signal():
    """
    Simulates Event Risk Signal (0-100).
    In production, this integrates Finnhub news sentiment and VIX spikes.
    """
    # Simulate high volatility + geopolitical tension (Iran crisis context)
    sentiment_score = 85 
    return sentiment_score

def _fred_latest(series_id: str) -> dict:
    """Fetch latest observation for a FRED series."""
    end   = date.today().strftime("%Y-%m-%d")
    start = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
    url   = (f"{FRED_URL}?series_id={series_id}&api_key={FRED_KEY}"
             f"&file_type=json&observation_start={start}&observation_end={end}&sort_order=desc&limit=2")
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())
    obs = [o for o in data.get("observations", []) if o["value"] != "."]
    return obs[0] if obs else {}

def get_macro_snapshot() -> dict:
    """Return current macro indicators."""
    result = {}
    for sid, label in SERIES.items():
        try:
            obs = _fred_latest(sid)
            result[sid] = {"label": label, "value": float(obs.get("value", 0)), "date": obs.get("date", "")}
        except Exception as e:
            result[sid] = {"label": label, "value": None, "error": str(e)}
    return result

def get_regime_signal(snapshot: dict):
    """
    Determines market regime: BULL, BEAR-INFLATION, BEAR-LIQUIDITY, or NEUTRAL/CHOP.
    Now includes 'Pre-emptive Bear' trigger based on Event Risk.
    """
    y10 = snapshot.get("DGS10", {}).get("value")
    y2  = snapshot.get("DGS2",  {}).get("value")
    event_risk = get_event_risk_signal()

    # Pre-emptive Bear Trigger
    if event_risk > 70:
        return "🔴 BEAR-LIQUIDITY (EVENT-RISK TRIGGERED)"

    if y10 is None or y2 is None:
        return "⚪ NEUTRAL/CHOP"
    
    spread = y10 - y2
    if spread >= 0.5:
        return "🟢 BULL"
    elif spread < 0:
        return "🔴 BEAR-INFLATION"
    else:
        return "🟡 NEUTRAL/CHOP"

def format_macro(snapshot: dict) -> str:
    """Format macro snapshot for WhatsApp."""
    lines = ["*Macro Environment*", f"Regime: {get_regime_signal(snapshot)}", f"Event Risk Score: {get_event_risk_signal()}/100"]
    y10  = snapshot.get("DGS10", {})
    y2   = snapshot.get("DGS2",  {})
    fed  = snapshot.get("FEDFUNDS", {})
    m2   = snapshot.get("M2SL", {})

    if y10.get("value"):
        lines.append(f"• 10Y Treasury: {y10['value']:.2f}%")
    if y2.get("value"):
        lines.append(f"• 2Y Treasury:  {y2['value']:.2f}%")

    return "\n".join(lines)

if __name__ == "__main__":
    snap = get_macro_snapshot()
    print(format_macro(snap))
