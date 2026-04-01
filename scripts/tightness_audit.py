import yfinance as yf
import pandas as pd
import json

# Universe
SYMBOLS = ['NVDA', 'AMD', 'META', 'AMZN', 'MSFT', 'CRWD', 'DDOG', 'MDB', 'NET', 'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'PATH', 'ESTC']

def run_tightness_audit(symbol):
    try:
        df = yf.Ticker(symbol).history(period="2y")
        if len(df) < 200: return []
        
        # Institutional Tightness Indicators
        df['Vol_Mean'] = df['Volume'].rolling(20).mean()
        df['Vol_Std'] = df['Volume'].rolling(20).std()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        vectors = []
        for i in range(200, len(df) - 10):
            # 1. Structural Trend
            if df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. Institutional Tightness (Vol_Std / Vol_Mean < 0.25 - Highly consistent volume)
            vol_tightness = df['Vol_Std'].iloc[i] / df['Vol_Mean'].iloc[i]
            # 3. ATR Tightness (ATR < 2% of price)
            atr_tightness = df['ATR14'].iloc[i] / df['Close'].iloc[i]
            
            if vol_tightness < 0.25 and atr_tightness < 0.02:
                # Signal: Breakout of this tightness
                if df['Close'].iloc[i] > df['High'].iloc[i-5:i].max():
                    ret = ((df['Close'].iloc[i+10] / df['Close'].iloc[i]) - 1) * 100
                    vectors.append({"symbol": symbol, "return": round(ret, 2)})
        return vectors
    except: return []

results = []
for s in SYMBOLS:
    results.extend(run_tightness_audit(s))

wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
print(json.dumps({"success_rate": round(success_rate, 2), "total": len(results)}, indent=4))
