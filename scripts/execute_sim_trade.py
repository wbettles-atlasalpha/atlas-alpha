import json
from sim_engine import load_portfolio, execute_trade
from macro_scan import get_macro_snapshot, get_regime_signal

# Target Weights for BEAR-LIQUIDITY Regime
TARGET_WEIGHTS = {
    "XLE": 0.35,
    "XLP": 0.30,
    "XLV": 0.20,
    "SHV": 0.15
}

# Current Prices (Simulation uses these as fixed current prices for now)
PRICES = {
    "XLE": 105.0,
    "XLP": 75.0,
    "XLV": 150.0,
    "SHV": 110.0
}

def dry_run():
    p = load_portfolio()
    total_val = p['cash'] + sum(qty * PRICES.get(sym, 0) for sym, qty in p['positions'].items())
    
    print(f"--- Dry Run: {get_regime_signal(get_macro_snapshot())} ---")
    print(f"Total Portfolio Value: ${total_val:.2f}")
    
    trades = []
    for sym, weight in TARGET_WEIGHTS.items():
        target_val = total_val * weight
        current_val = p['positions'].get(sym, 0) * PRICES.get(sym, 0)
        diff = target_val - current_val
        
        if abs(diff) > 100: # Ignore noise
            qty = round(abs(diff) / PRICES[sym], 2)
            side = "buy" if diff > 0 else "sell"
            trades.append((sym, qty, side, PRICES[sym]))
            print(f"Proposed: {side} {qty} {sym} @ ${PRICES[sym]}")
            
    return trades

if __name__ == "__main__":
    confirm = input("Execute trades? (y/n): ")
    if confirm.lower() == 'y':
        trades = dry_run()
        for sym, qty, side, price in trades:
            execute_trade(sym, qty, side, price)
    else:
        dry_run()
        print("Dry run complete. No trades executed.")
