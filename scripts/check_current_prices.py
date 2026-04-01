from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 4002, clientId=4)

# Define contracts
contracts = {
    "NET": Stock('NET', 'SMART', 'USD'),
    "LUNR": Stock('LUNR', 'SMART', 'USD')
}

for sym, con in contracts.items():
    ticker = ib.reqMktData(con, '', False, False)
    ib.sleep(1)
    price = ticker.last if ticker.last > 0 else ticker.close
    print(f"{sym}: {price}")

ib.disconnect()
