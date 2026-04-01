import yfinance as yf
import pandas as pd
import json

# Universe (Broad S&P 500 representation)
SYMBOLS = ["JPM", "V", "BRK-B", "JNJ", "WMT", "PG", "HD", "CVX", "MRK", "ABBV", "KO", "PEP", "BAC", "PFE", "COST", "MCD", "TMO", "ABT", "DHR", "LLY"]

def reverse_engineer_winners():
    winners = []
    
    for sym in SYMBOLS:
        try:
            df = yf.Ticker(sym).history(start="2025-01-01", end="2025-12-31")
            if len(df) < 50: continue
            
            df['VolMA20'] = df['Volume'].rolling(20).mean()
            df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
            
            # Look for 7-day growth windows
            for i in range(20, len(df) - 8):
                ret = ((df['Close'].iloc[i+7] / df['Close'].iloc[i]) - 1) * 100
                
                # Pre-growth stats (14 days prior to growth start)
                pre_vol_ratio = df['Volume'].iloc[i-14:i].mean() / df['VolMA20'].iloc[i]
                pre_atr_ratio = df['ATR14'].iloc[i] / df['Close'].iloc[i]
                
                winners.append({
                    "symbol": sym,
                    "return": round(ret, 2),
                    "pre_vol_ratio": round(pre_vol_ratio, 3),
                    "pre_atr_ratio": round(pre_atr_ratio, 4)
                })
        except: continue
        
    top_winners = sorted(winners, key=lambda x: x['return'], reverse=True)[:50]
    
    avg_vol = sum([w['pre_vol_ratio'] for w in top_winners]) / len(top_winners)
    avg_atr = sum([w['pre_atr_ratio'] for w in top_winners]) / len(top_winners)
    
    return {
        "analysis": {
            "avg_pre_vol_ratio": round(avg_vol, 3),
            "avg_pre_atr_ratio": round(avg_atr, 4)
        },
        "top_examples": top_winners[:5]
    }

print(json.dumps(reverse_engineer_winners(), indent=4))
