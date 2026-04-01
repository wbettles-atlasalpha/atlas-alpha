# Atlas Alpha - Backtesting Roadmap

1. **Backtesting Framework (Priority: High)**
   - Build local Python harness in `backtest/` to stress-test "Alpha Vector" logic against historical data (`PORTFOLIO_LEDGER.csv` + MarketStack API).
   - Aim: Generate "Performance Audit" for transparency before launch.

2. **Sentiment Aggregation (Priority: Medium)**
   - Integrate Finnhub API to track real-time sentiment divergence from volume anomalies.
   - Use to flag potential invalidation triggers.

3. **Macro Regime Mapping (Priority: Low)**
   - FRED (Federal Reserve) API integration to automate position sizing based on macro liquidity (Fed Funds Rate, M2 Supply).

4. **Institutional Flow Tracking (Roadmap)**
   - Dark Pool/Off-Exchange TRF monitoring (e.g., Unusual Whales).
   - Cost: ~$100 USD/mo.
   - Note: Hold until we generate revenue.
