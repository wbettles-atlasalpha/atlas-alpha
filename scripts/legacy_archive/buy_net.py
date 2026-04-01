from ib_insync import *

# Connect
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=1)

# Place NET buy order (90 shares)
contract = Stock('NET', 'SMART', 'USD')
order = MarketOrder('BUY', 90)
trade = ib.placeOrder(contract, order)

print(f"Order placed: {trade}")

ib.disconnect()
