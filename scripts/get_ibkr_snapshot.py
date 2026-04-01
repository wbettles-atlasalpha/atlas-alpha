from ib_insync import *

# Connect
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=2)

# Get positions
positions = ib.positions()
account_values = ib.accountSummary()

print("Current Positions:")
for p in positions:
    print(f"{p.contract.symbol}: {p.position}")

print("\nAccount Values:")
for v in account_values:
    if v.tag == 'NetLiquidation':
        print(f"Net Liquidation: {v.value} {v.currency}")
    if v.tag == 'TotalCashValue':
        print(f"Total Cash: {v.value} {v.currency}")

ib.disconnect()
