
import yfinance as yf
import pandas as pd
import numpy as np

# We'll use a representative basket to simulate index scanning
symbols = ['PNR', 'HII', 'MTZ', 'FSLR', 'ZBRA', 'STE', 'AJG', 'TYL', 'RGLD', 'CBOE', 'FICO', 'PKG', 'TDG', 'AFL']
index_spy = yf.Ticker("SPY")
hist_spy = index_spy.history(period="10y")

def backtest_criteria(symbols):
    results = []
    
    for s in symbols:
        ticker = yf.Ticker(s)
        hist = ticker.history(period="10y")
        if len(hist) < 200: continue
            
        # Entry logic
        # 1. Price < 90% of 30d High
        # 2. Volume < 80% of 30d Avg
        # 3. Regime: Spy > 200 SMA
        for i in range(200, len(hist)-20):
            date = hist.index[i]
            if date not in hist_spy.index: continue
            
            # Check Regime
            sma200 = hist_spy.loc[:date].tail(200)['Close'].mean()
            if hist_spy.loc[date]['Close'] < sma200: continue
            
            # Check Entry
            high_30d = hist.loc[:date].tail(30)['High'].max()
            vol_30d = hist.loc[:date].tail(30)['Volume'].mean()
            curr_close = hist.loc[date]['Close']
            curr_vol = hist.loc[date]['Volume']
            
            if curr_close < (high_30d * 0.90) and curr_vol < (vol_30d * 0.8):
                entry = curr_close
                # 20% TP or 5% Trailing SL
                peak = entry
                for j in range(1, 20):
                    if i+j >= len(hist): break
                    exit = hist['Close'].iloc[i+j]
                    if exit > peak: peak = exit
                    if exit >= entry * 1.20:
                        results.append({'pnl': 0.20, 'win': 1})
                        break
                    elif exit <= peak * 0.95:
                        pnl = (exit/entry)-1
                        results.append({'pnl': pnl, 'win': 1 if pnl > 0 else 0})
                        break
    return pd.DataFrame(results)

df = backtest_criteria(symbols)
print(f"Total Vectors Identified: {len(df)}")
print(f"Win Rate: {df['win'].mean() * 100:.2f}%")
print(f"Avg PnL: {df['pnl'].mean() * 100:.2f}%")
