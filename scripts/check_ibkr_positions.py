from ib_insync import *

# Connect
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=1)

# Get positions
positions = ib.positions()
print("Current Positions:")
for p in positions:
    print(f"{p.contract.symbol}: {p.position}")

ib.disconnect()
