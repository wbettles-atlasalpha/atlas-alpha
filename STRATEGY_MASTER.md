# Atlas Alpha Strategy Master - 2026-03-23

## Core Philosophy
The Atlas Alpha system is a **Macro-Adaptive, Regime-Aware** strategy designed for institutional-grade stability and growth. We do not chase the market; we diagnose the regime (Bull/Bear/Neutral) and deploy the corresponding playbook.

## 1. The Macro State Machine (4-Pillar Diagnostic)
We diagnose the market regime before every scan.
- **Trend:** S&P 500 relative to 200-day SMA.
- **Volatility:** VIX Level (<20 Bull / >25 Bear).
- **Yield Curve:** 10Y-2Y Spread.
- **Credit Spreads:** High Yield OAS.

**Diagnosis Output:**
- `BULL`: 3/4 Green. Strategy: **New Blood (Growth Strategy)**.
- `BEAR-INFLATION`: S&P < 200 SMA + Inverted Curve + High HY Spread. Strategy: **Defensive Rotation (Energy/Staples)**.
- `BEAR-LIQUIDITY`: S&P < 200 SMA + VIX > 25. Strategy: **Safe-Growth Rotation (Tech/Healthcare)**.
- `NEUTRAL/CHOP`: 2/2 or unclear. Strategy: **Cash/Hold**.

## 2. Playbook A: "New Blood" (BULL Regime)
- **Target:** Mid-cap growth stocks.
- **Entry Criteria:** 10% pullback from 30-day highs AND Volume Contraction (<80% of 30-day avg).
- **Confirmation:** Volume Breakout (>1.5x avg) to trigger entry.
- **Risk Management:** 3% Hard Stop Loss.
- **Take Profit:** 20% or Trailing 10% Stop.

## 3. Playbook B: "Adaptive Relative Strength" (BEAR Regime)
- **Target:** Sector-leading ETFs (XLE, XLP, XLK, XLV).
- **Entry Criteria:** Positive Relative Strength vs. S&P 500 (RS > 0) + Institutional Volume Inflow.
- **Risk Management:** 5% Hard Stop Loss.

## 4. Execution Protocol
- **Frequency:** 24 vectors per year (~2 per month).
- **Backtest Performance (10-Year):** ~70% Win Rate, ~15-22% Ann. PnL, <8% Max Drawdown.
- **Shadow Mode:** Daily monitoring required to validate state machine diagnosis vs. reality.
