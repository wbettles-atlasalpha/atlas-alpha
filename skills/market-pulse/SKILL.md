---
name: market-pulse
description: Institutional-grade stock analysis and volume spike detection. Use this skill when the user wants to scan the market for volume anomalies, analyze stock tickers, or generate an Atlas Alpha Invalidation Thesis. Trigger on phrases like "run a market pulse", "scan the market", "check volume spikes", or when asked to analyze specific stocks for the Atlas Alpha portfolio.
---

# Market Pulse

This skill provides the core analytical engine for Atlas Alpha, focusing on identifying volume anomalies and building high-conviction trade theses with explicit invalidation parameters.

## Capabilities

### 1. Volume Spikes Scan
To hunt for institutional liquidity shifts and volume anomalies, execute the `volume_scan.py` script.

```bash
FINNHUB_API_KEY="your_finnhub_key" ALPHAVANTAGE_API_KEY="your_alpha_key" python3 /home/warwick/.openclaw/workspace/skills/market-pulse/scripts/volume_scan.py [TICKERS] [THRESHOLD]
```
- **TICKERS**: A comma-separated list of stock tickers (e.g., `AAPL,TSLA,ZETA`). If omitted, it defaults to a standard tech watchlist.
- **THRESHOLD**: The volume ratio threshold (e.g., `1.5` for 150% of the 10-day average).

### 2. Macro Pulse Scan
To scan the Global Macro indicators (Federal Funds Rate, Yield Curve, M2 Money Supply), execute the `macro_scan.py` script.

```bash
FRED_API_KEY="your_fred_key" python3 /home/warwick/.openclaw/workspace/skills/market-pulse/scripts/macro_scan.py
```

### 3. PDF Analysis (Catalyst Validation)
When a volume spike is detected, the next step is catalyst validation. Use your native PDF reading abilities (via the `read` tool) to process 10-K, 10-Q, or earnings call transcript PDFs to cross-reference the volume action against real-world fundamentals.

### 3. The Invalidation Thesis Generation
When the user asks you to write an Atlas Alpha "Signal Thesis Card" for a stock, follow the strict Atlas Alpha format:

1. **Category**: Define the asset class (e.g., "Semiconductor AI Infrastructure", "Quantum Computing Speculative").
2. **Pill**: Assign a conviction pillar: `Core`, `Growth`, `Moonshot`, or `Value/Growth`.
3. **Badge**: Assign a rating: `STRONG BUY`, `BUY`, or `BUY SPEC`.
4. **Thesis**: Write a concise, institutional-grade paragraph explaining the catalyst.
5. **Invalidation**: Provide a specific, hard price point or macro event that kills the trade (e.g., "Break below $206 (Gap Fill)").

## Workflow

1. Scan for volume spikes using `scripts/volume_scan.py`.
2. Review relevant PDFs/reports for the flagged tickers.
3. Generate the Atlas Alpha Invalidation Thesis and output it to the user.