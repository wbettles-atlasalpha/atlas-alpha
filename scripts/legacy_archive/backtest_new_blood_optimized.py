
import yfinance as yf
import pandas as pd

def backtest_new_blood_strategy(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="10y")
    
    signals = []
    # Entry: 10% pullback from 30d high + vol contraction
    # Exit: 20% TP or Trailing Stop Loss (5%)
    for i in range(30, len(hist)-20):
        high_30d = hist['High'].iloc[i-30:i].max()
        vol_30d = hist['Volume'].iloc[i-30:i].mean()
        
        if hist['Close'].iloc[i] < (high_30d * 0.90) and hist['Volume'].iloc[i] < (vol_30d * 0.8):
            entry_price = hist['Close'].iloc[i]
            peak_price = entry_price
            
            # Simulate holding with Trailing Stop
            trade_closed = False
            for j in range(1, 20): # Look ahead up to 20 days
                if i+j < len(hist):
                    curr_price = hist['Close'].iloc[i+j]
                    
                    # Update peak for trailing stop
                    if curr_price > peak_price:
                        peak_price = curr_price
                    
                    # TP 20%
                    if curr_price >= entry_price * 1.20:
                        signals.append({'pnl': 0.20, 'win': 1})
                        trade_closed = True
                        break
                    # Trailing SL 5% from peak
                    elif curr_price <= peak_price * 0.95:
                        pnl = (curr_price / entry_price) - 1
                        signals.append({'pnl': pnl, 'win': 1 if pnl > 0 else 0})
                        trade_closed = True
                        break
            if not trade_closed:
                final_pnl = (hist['Close'].iloc[min(i+20, len(hist)-1)] / entry_price) - 1
                signals.append({'pnl': final_pnl, 'win': 1 if final_pnl > 0 else 0})
                
    return signals

# Using a basket representing mid-cap indices (S&P 400 components)
symbols = ['PNR', 'HII', 'MTZ', 'FSLR', 'ZBRA', 'STE', 'AJG', 'TYL', 'RGLD', 'CBOE']
results = []
for s in symbols:
    results.extend(backtest_new_blood_strategy(s))

df = pd.DataFrame(results)
print(f"Total Vectors: {len(df)}")
print(f"Win Rate: {df['win'].mean() * 100:.2f}%")
print(f"Avg PnL: {df['pnl'].mean() * 100:.2f}%")
