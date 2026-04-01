# HEARTBEAT.md

# Atlas Alpha Daily Operations Checklist

When the heartbeat triggers:
1. Briefly review `memory/YYYY-MM-DD.md` to ensure nothing broke since yesterday.
2. If it is close to 8:30 AM (Melbourne time), confirm the master cron job is scheduled correctly to run the Paper Portfolio, by cross-referencing with the system schedule or ensuring the `cron` package is installed, and deliver the Morning Brief. 
3. If Warwick asks for an on-demand analysis of a ticker, use `scripts/volume_scan.py` and `scripts/macro_scan.py` to generate an Invalidation Thesis instantly.
4. If there's nothing urgent and no user prompts, reply strictly with: `HEARTBEAT_OK`