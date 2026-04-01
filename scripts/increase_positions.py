from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 4002, clientId=6)

# NET: Current 90. Need ~903 total. Buy 813 more.
contract_net = Stock('NET', 'SMART', 'USD')
trade_net = ib.placeOrder(contract_net, MarketOrder('BUY', 813, tif='GTC'))
print(f"NET order: {trade_net}")

# LUNR: Current 1057. Need ~10576 total. Buy 9519 more.
contract_lunr = Stock('LUNR', 'SMART', 'USD')
trade_lunr = ib.placeOrder(contract_lunr, MarketOrder('BUY', 9519, tif='GTC'))
print(f"LUNR order: {trade_lunr}")

ib.disconnect()
