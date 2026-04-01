import yfinance as yf
import pandas as pd
import json

# Universe
# FTSE 100 (Simplified sample)
# ASX 200 (Simplified sample)
UNIVERSE = {
    "FTSE 100": ["HSBA.L", "BP.L", "SHEL.L", "AZN.L", "GSK.L", "RIO.L", "BATS.L", "ULVR.L", "NG.L", "DGE.L"],
    "ASX 200": ["BHP.AX", "CBA.AX", "CSL.AX", "NAB.AX", "WBC.AX", "ANZ.AX", "WDS.AX", "RIO.AX", "MQG.AX", "WOW.AX"]
}

def reverse_engineer_winners():
    results = {}
    for universe, symbols in UNIVERSE.items():
        winners = []
        for sym in symbols:
            try:
                df = yf.Ticker(sym).history(start="2025-01-01", end="2025-12-31")
                if len(df) < 50: continue
                
                df['VolMA20'] = df['Volume'].rolling(20).mean()
                df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
                
                for i in range(20, len(df) - 8):
                    ret = ((df['Close'].iloc[i+7] / df['Close'].iloc[i]) - 1) * 100
                    pre_vol_ratio = df['Volume'].iloc[i-14:i].mean() / df['VolMA20'].iloc[i]
                    pre_atr_ratio = df['ATR14'].iloc[i] / df['Close'].iloc[i]
                    
                    winners.append({"return": ret, "pre_vol": pre_vol_ratio, "pre_atr": pre_atr_ratio})
            except: continue
            
        top = sorted(winners, key=lambda x: x['return'], reverse=True)[:50]
        results[universe] = {
            "avg_vol": round(sum([w['pre_vol'] for w in top]) / len(top), 3),
            "avg_atr": round(sum([w['pre_atr'] for w in top]) / len(top), 4)
        }
    return results

print(json.dumps(reverse_engineer_winners(), indent=4))
