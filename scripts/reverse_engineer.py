import yfinance as yf
import pandas as pd
import json

# Universe (Nasdaq 100 sample)
SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "AVGO", "TSLA", "COST", "PEP", "ADBE", "AMD", "NFLX", "INTC", "CSCO"]

def reverse_engineer_winners():
    winners = []
    
    for sym in SYMBOLS:
        try:
            df = yf.Ticker(sym).history(start="2025-01-01", end="2025-12-31")
            if len(df) < 50: continue
            
            df['VolMA20'] = df['Volume'].rolling(20).mean()
            df['EMA50'] = df['Close'].ewm(span=50).mean()
            df['EMA200'] = df['Close'].ewm(span=200).mean()
            df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
            
            # Look for 7-day growth windows
            for i in range(200, len(df) - 8):
                ret = ((df['Close'].iloc[i+7] / df['Close'].iloc[i]) - 1) * 100
                
                # Pre-growth stats (14 days prior to growth start)
                if i < 14: continue
                pre_vol_ratio = df['Volume'].iloc[i-14:i].mean() / df['VolMA20'].iloc[i]
                pre_atr_ratio = df['ATR14'].iloc[i] / df['Close'].iloc[i]
                
                winners.append({
                    "symbol": sym,
                    "return": round(ret, 2),
                    "pre_vol_ratio": round(pre_vol_ratio, 3),
                    "pre_atr_ratio": round(pre_atr_ratio, 4)
                })
        except: continue
        
    # Get top 100 winners
    top_100 = sorted(winners, key=lambda x: x['return'], reverse=True)[:100]
    
    # Analyze common denominators
    avg_vol = sum([w['pre_vol_ratio'] for w in top_100]) / len(top_100)
    avg_atr = sum([w['pre_atr_ratio'] for w in top_100]) / len(top_100)
    
    return {
        "analysis": {
            "avg_pre_vol_ratio": round(avg_vol, 3),
            "avg_pre_atr_ratio": round(avg_atr, 4)
        },
        "top_examples": top_100[:10]
    }

print(json.dumps(reverse_engineer_winners(), indent=4))
