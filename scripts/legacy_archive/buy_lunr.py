from ib_insync import *

# Connect
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=1)

# Place LUNR buy order (1057 shares)
contract = Stock('LUNR', 'SMART', 'USD')
order = MarketOrder('BUY', 1057)
trade = ib.placeOrder(contract, order)

print(f"Order placed for LUNR: {trade}")

ib.disconnect()
