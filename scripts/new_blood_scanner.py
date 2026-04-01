
import pandas as pd
import yfinance as yf
import numpy as np

def scan_for_new_blood():
    # Exclude list of familiar/failed tickers
    exclude_list = ['RKLB', 'ZETA', 'VKTX', 'CRWD', 'DDOG', 'MDB', 'NET', 'APP', 'NVDA', 'AAPL', 'MSFT', 'AMZN']
    
    # Simple list of candidates to test (broadening to mid-cap focus)
    # In a real run, this would be a market-wide S&P 400/Smallcap 600 scan
    candidates = ['PATH', 'ASAN', 'IOT', 'TTD', 'PLTR', 'U', 'COIN', 'TOST', 'DUOL', 'BRZE', 'SNOW', 'MNDY', 'BILL', 'AFRM', 'DOCU', 'ZM', 'PTON', 'FSLY', 'ESTC', 'DT']
    
    found_vectors = []
    
    print(f"Scanning for new blood, excluding: {exclude_list}")
    
    for symbol in candidates:
        if symbol in exclude_list:
            continue
            
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")
            
            if hist.empty or hist['Volume'].mean() < 10000000: # Liquidity filter
                continue
            
            # Correction filter: Current price < 90% of 30-day high (10% pullback)
            high_30d = hist['High'].tail(30).max()
            current = hist['Close'].iloc[-1]
            
            if current < (high_30d * 0.90): # Healthy 10%+ pullback
                # Volume contraction filter (current vol < 80% of 30-day avg)
                vol_30d = hist['Volume'].tail(30).mean()
                current_vol = hist['Volume'].iloc[-1]
                
                if current_vol < (vol_30d * 0.8):
                    found_vectors.append({'symbol': symbol, 'price': current, 'reason': '10% pullback + volume contraction'})
                    
        except Exception as e:
            continue
            
    return found_vectors

results = scan_for_new_blood()
print(results)
