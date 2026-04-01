from ib_insync import *

# Atlas Alpha: IBKR Execution Engine
# Connect to TWS/Gateway
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=1)

def execute_order(symbol, qty, side):
    contract = Stock(symbol, 'SMART', 'USD')
    # Validate contract
    details = ib.reqContractDetails(contract)
    if not details:
        print(f"Error: Contract {symbol} not found.")
        return
    
    contract = details[0].contract
    order = MarketOrder(side.upper(), qty)
    trade = ib.placeOrder(contract, order)
    
    # Wait for completion
    ib.sleep(2)
    print(f"Executed {side} order for {qty} shares of {symbol}. Status: {trade.orderStatus.status}")

try:
    print("Executing rotation to ASTS...")
    execute_order('ASTS', 111, 'BUY')
    
except Exception as e:
    print(f"Execution Error: {e}")
finally:
    ib.disconnect()
