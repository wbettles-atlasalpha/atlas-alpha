# Local Trading Simulation Engine (Atlas Alpha)

## Core Design Goals
1. **Deterministic Execution:** No more API failures. The simulation engine processes trades internally using real-time (or historical) data feeds.
2. **Account State:** Track cash, positions, and unrealized P&L in a local JSON state file (`SIM_PORTFOLIO.json`).
3. **Execution Module:** Replace `alpaca_buy.py` with `sim_execute.py` that updates the local state rather than hitting an external API.

## Implementation Path
- **State File:** `SIM_PORTFOLIO.json` stores current holdings and cash balance.
- **Data Feed:** Use our existing `Finnhub` / `MarketStack` connections for live pricing.
- **Engine Logic:**
    - `sim_trade(symbol, qty, side, price)`: Calculates total cost, updates cash, adjusts position quantities.
    - `get_valuation()`: Aggregates current holdings * last price for NAV calculation.
- **Interface:** Same CLI interface as current scripts, allowing seamless transition to live trading later.

## Benefits
- **Zero Latency/Failure:** The "trade" happens in memory.
- **Auditability:** Every transaction is logged locally with a timestamp and reason (e.g., "Macro Signal: BEAR-LIQUIDITY").
- **Backtesting parity:** We can test the strategy using real-time data against our own engine, then swap the "backend" to a live exchange later.

Shall I prototype the `sim_execute.py` engine today, or should we define the JSON structure for the portfolio state first? 🛡️