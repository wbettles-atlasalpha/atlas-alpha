import yfinance as yf
import pandas as pd
import math

# Compound Audit: $1,000 starting
# 57 vectors identified, avg return 8.05% per 5-day cycle.

initial = 1000
signals = 57
avg_ret = 0.0805 # 8.05%

# Compound growth assuming 100% of capital deployed each time (Theoretical Max)
compounded_max = initial * ((1 + avg_ret) ** signals)

# Compound growth assuming 20% of capital deployed each time (Risk Managed)
# Formula: (Capital * (1 - 0.2)) + (Capital * 0.2 * (1 + 0.0805))
# This is a bit complex for a quick calc, let's use a simpler iterative model
capital = initial
for _ in range(signals):
    # Deploy 20% into the signal
    invested = capital * 0.20
    cash = capital * 0.80
    return_on_invest = invested * (1 + avg_ret)
    capital = cash + return_on_invest

print(f"--- Compounding Projection ($1,000 initial, {signals} signals) ---")
print(f"Theoretical Max (100% allocation): ${compounded_max:,.2f}")
print(f"Risk Managed (20% allocation per signal): ${capital:,.2f}")
