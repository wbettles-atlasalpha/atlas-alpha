import yfinance as yf
import pandas as pd

tickers = ['AAPL', 'MSFT', 'NVDA', 'ASTS', 'VKTX', 'TSLA', 'AMD', 'PLTR', 'RKLB', 'CRWD', 'UBER', 'SOFI', 'ZETA', 'IONQ', 'META', 'AMZN', 'GOOGL', 'AVGO']

for symbol in tickers:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1y") # Get more data
    if len(hist) < 30: continue
    
    hist['MA_Vol'] = hist['Volume'].rolling(window=30).mean()
    
    # Just print the first trigger found
    for i in range(30, len(hist) - 1):
        if hist.iloc[i]['Volume'] > (1.5 * hist.iloc[i]['MA_Vol']):
            print(f"{symbol} trigger at {hist.index[i].strftime('%Y-%m-%d')} Volume {hist.iloc[i]['Volume']} MA {hist.iloc[i]['MA_Vol']}")
            break
