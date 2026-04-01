
import yfinance as yf
import pandas as pd

def backtest_new_blood_strategy(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="10y")
    
    signals = []
    # Entry: 10% pullback from 30d high + vol contraction
    # Exit: 3% SL or 5% TP
    for i in range(30, len(hist)-10):
        high_30d = hist['High'].iloc[i-30:i].max()
        vol_30d = hist['Volume'].iloc[i-30:i].mean()
        
        if hist['Close'].iloc[i] < (high_30d * 0.90) and hist['Volume'].iloc[i] < (vol_30d * 0.8):
            entry_price = hist['Close'].iloc[i]
            
            # Simulate holding
            trade_closed = False
            for j in range(1, 10): # Look ahead up to 10 days
                if i+j < len(hist):
                    exit_price = hist['Close'].iloc[i+j]
                    if exit_price >= entry_price * 1.05: # TP 5%
                        signals.append({'pnl': 0.05, 'win': 1})
                        trade_closed = True
                        break
                    elif exit_price <= entry_price * 0.97: # SL 3%
                        signals.append({'pnl': -0.03, 'win': 0})
                        trade_closed = True
                        break
            if not trade_closed:
                # Close at end of window
                final_pnl = (hist['Close'].iloc[min(i+10, len(hist)-1)] / entry_price) - 1
                signals.append({'pnl': final_pnl, 'win': 1 if final_pnl > 0 else 0})
                
    return signals

symbols = ['U', 'PATH', 'ASAN', 'IOT', 'TTD', 'PLTR']
results = []
for s in symbols:
    results.extend(backtest_new_blood_strategy(s))

df = pd.DataFrame(results)
print(f"Total Vectors: {len(df)}")
print(f"Win Rate: {df['win'].mean() * 100:.2f}%")
print(f"Avg PnL: {df['pnl'].mean() * 100:.2f}%")
