import json
import csv

# We are analyzing 6 months of simulated data for high-beta tickers.
# This simulation generates the "Audit Log" output.

def run_audit():
    # Mock data structure to mimic Atlas Alpha "Market Vector" results
    # Real-world integration will pull from MarketStack historical OHLCV data.
    signals = [
        {"ticker": "NVDA", "identified": "2025-10-12", "entry": 120.00, "invalidation": 114.00, "status": "Closed", "exit": 155.00, "return": 29.1},
        {"ticker": "ASTS", "identified": "2025-11-05", "entry": 22.50, "invalidation": 21.37, "status": "Closed", "exit": 21.00, "return": -6.6},
        {"ticker": "TSLA", "identified": "2026-01-15", "entry": 240.00, "invalidation": 228.00, "status": "Closed", "exit": 280.00, "return": 16.6},
        {"ticker": "AMD", "identified": "2026-02-02", "entry": 155.00, "invalidation": 147.25, "status": "Active", "exit": None, "return": 4.2}
    ]

    print("| Ticker | Identified Date | Entry Price | Invalidation Point | Status | Exit Price | Return % |")
    print("|---|---|---|---|---|---|---|")
    total_return = 0
    closed_count = 0
    for s in signals:
        exit_val = s['exit'] if s['exit'] else "N/A"
        print(f"| {s['ticker']} | {s['identified']} | ${s['entry']:.2f} | ${s['invalidation']:.2f} | {s['status']} | {exit_val} | {s['return']}% |")
        if s['status'] == 'Closed':
            total_return += s['return']
            closed_count += 1

    print("\n--- Summary ---")
    print(f"Total Vectors Identified: {len(signals)}")
    print(f"Avg Return (Closed): {(total_return/closed_count):.2f}%")

if __name__ == "__main__":
    run_audit()
