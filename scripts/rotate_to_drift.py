from ib_insync import *

# Atlas Alpha: Discipline Rotation
# 1. Liquidate NET (903 shares), LUNR (10576 shares)
# 2. Buy PLTR, DDOG, ASTS to ~$100k AUD target per position.

ib = IB()
ib.connect('127.0.0.1', 4002, clientId=1)

def execute_order(symbol, qty, side):
    contract = Stock(symbol, 'SMART', 'USD')
    details = ib.reqContractDetails(contract)
    if not details:
        print(f"Error: Contract {symbol} not found.")
        return
    
    contract = details[0].contract
    order = MarketOrder(side.upper(), qty)
    trade = ib.placeOrder(contract, order)
    ib.sleep(2)
    print(f"Executed {side} order for {qty} shares of {symbol}. Status: {trade.orderStatus.status}")

try:
    # 1. Liquidate
    print("--- Liquidating Positions ---")
    execute_order('NET', 903, 'SELL')
    execute_order('LUNR', 10576, 'SELL')
    
    # 2. Buy/Rebalance (Estimates based on current approximate prices)
    print("--- Executing Drift Rotation ---")
    # Targets: ~100k AUD per position
    # Prices (approx): ASTS~$137 AUD, PLTR~$230 AUD, DDOG~$192 AUD
    # ASTS shares to add: Target ~730 total. Currently have 111. Add ~619.
    execute_order('ASTS', 619, 'BUY')
    
    # PLTR shares: Target ~435.
    execute_order('PLTR', 435, 'BUY')
    
    # DDOG shares: Target ~520.
    execute_order('DDOG', 520, 'BUY')
    
except Exception as e:
    print(f"Execution Error: {e}")
finally:
    ib.disconnect()
