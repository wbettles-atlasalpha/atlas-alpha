"""
Atlas Alpha - Reddit Sniper
Finds threads on r/investing, r/stocks, r/ASX, r/ausstocks where Warwick
can add genuine value and subtly promote Atlas Alpha.

Uses Reddit's public JSON API (no auth required for read-only access).
For posting, Reddit OAuth credentials can be added to TOOLS.md when ready.
"""

import urllib.request, json, time
from datetime import datetime, timezone

SUBREDDITS = [
    "investing",
    "stocks",
    "StockMarket",
    "ausstocks",
    "ASX_Bets",
    "pennystocks",
]

# Keywords that signal a post where Atlas Alpha analysis adds value
SIGNAL_KEYWORDS = [
    "buy or sell", "what do you think", "is it too late", "entry point",
    "should i buy", "analysis", "thesis", "invalidation", "stop loss",
    "volume spike", "catalyst", "undervalued", "overvalued", "hold or sell",
    "next week", "earnings play", "technical analysis", "dd", "due diligence",
    "advice", "opinion", "thoughts on", "portfolio review",
]

# Keywords to avoid (low quality / not our audience)
SKIP_KEYWORDS = [
    "meme", "yolo", "ape", "moon", "tendies", "wsb", "short squeeze",
    "get rich quick", "pump", "crypto", "bitcoin", "doge",
]


def _reddit_get(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AtlasAlpha/1.0 (research bot; contact atlas@atlasalpha.io)"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def fetch_hot_posts(subreddit: str, limit: int = 25) -> list:
    """Fetch hot posts from a subreddit using Reddit's public JSON API."""
    url  = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    data = _reddit_get(url)
    posts = []
    for child in data.get("data", {}).get("children", []):
        p = child.get("data", {})
        posts.append({
            "subreddit":  subreddit,
            "title":      p.get("title", ""),
            "score":      p.get("score", 0),
            "comments":   p.get("num_comments", 0),
            "url":        f"https://reddit.com{p.get('permalink', '')}",
            "created":    p.get("created_utc", 0),
            "selftext":   (p.get("selftext") or "")[:500],
            "author":     p.get("author", ""),
        })
    return posts


def score_post(post: dict) -> int:
    """Score a post 0-100 for Atlas Alpha reply opportunity."""
    score     = 0
    text      = (post["title"] + " " + post["selftext"]).lower()

    # Skip low-quality posts
    for kw in SKIP_KEYWORDS:
        if kw in text:
            return 0

    # Signal keywords
    for kw in SIGNAL_KEYWORDS:
        if kw in text:
            score += 15

    # Engagement signals (worth replying to active threads)
    if post["score"] > 50:
        score += 10
    if post["comments"] > 20:
        score += 10
    if post["comments"] > 5:
        score += 5

    # Recency (posts within last 12h score higher)
    age_h = (time.time() - post["created"]) / 3600
    if age_h < 6:
        score += 20
    elif age_h < 12:
        score += 10
    elif age_h > 48:
        score -= 20

    return min(score, 100)


def run(top_n: int = 5) -> list:
    """
    Scan all subreddits and return top_n reply opportunities.
    Each result: {subreddit, title, score, url, opportunity_score, suggested_angle}
    """
    candidates = []

    for sub in SUBREDDITS:
        try:
            posts = fetch_hot_posts(sub, limit=25)
            for p in posts:
                opp_score = score_post(p)
                if opp_score >= 20:
                    candidates.append({**p, "opportunity_score": opp_score})
            time.sleep(1.5)  # Be polite to Reddit's API
        except Exception as e:
            print(f"  r/{sub}: {e}")

    candidates.sort(key=lambda x: x["opportunity_score"], reverse=True)
    top = candidates[:top_n]

    # Add suggested reply angle for each
    for lead in top:
        text = (lead["title"] + " " + lead["selftext"]).lower()
        if any(k in text for k in ["entry", "buy", "should i"]):
            lead["angle"] = "Offer invalidation level framework — lead with risk management"
        elif any(k in text for k in ["analysis", "dd", "thesis"]):
            lead["angle"] = "Add volume confirmation lens — complement their DD"
        elif any(k in text for k in ["portfolio", "review"]):
            lead["angle"] = "Offer portfolio construction perspective — diversification + catalyst check"
        else:
            lead["angle"] = "Add value with macro context and a specific insight"

    return top


def format_leads(leads: list) -> str:
    """Format leads as WhatsApp-friendly string."""
    if not leads:
        return "*Reddit Sniper*\nNo strong reply opportunities found today."

    lines = ["*Reddit Sniper — Reply Leads*"]
    for i, lead in enumerate(leads, 1):
        age_h = (time.time() - lead["created"]) / 3600
        lines.append(
            f"\n{i}. *r/{lead['subreddit']}* | Score {lead['opportunity_score']}/100\n"
            f"   _{lead['title'][:70]}_\n"
            f"   💬 {lead['comments']} comments | ⏱ {age_h:.0f}h ago\n"
            f"   Angle: {lead['angle']}\n"
            f"   🔗 {lead['url']}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print("Running Reddit Sniper...")
    leads = run(top_n=5)
    print(format_leads(leads))
