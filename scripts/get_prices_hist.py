from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 4002, clientId=5)

contracts = {
    "NET": Stock('NET', 'SMART', 'USD'),
    "LUNR": Stock('LUNR', 'SMART', 'USD')
}

for sym, con in contracts.items():
    bars = ib.reqHistoricalData(con, endDateTime='', durationStr='1 D', barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)
    if bars:
        price = bars[-1].close
        print(f"{sym}: {price}")
    else:
        print(f"{sym}: Could not retrieve price")

ib.disconnect()
