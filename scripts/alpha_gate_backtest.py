import yfinance as yf
import pandas as pd
import json

# Refined Universe (High-Growth/Fundamental Winners identified as "Institutional")
# These are stocks known for 20%+ Revenue Growth in 2025
UNIVERSE = ['NVDA', 'CRWD', 'MDB', 'NET', 'VKTX', 'ASTS', 'RKLB', 'ZETA', 'IONQ', 'APP']

def run_precision_backtest(symbol):
    try:
        # Load 2 years for context (2024-2025)
        df = yf.Ticker(symbol).history(start="2024-01-01", end="2025-12-31")
        if len(df) < 200: return []
        
        # Indicators
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = delta.clip(upper=0).abs()
        df['RSI'] = 100 - (100 / (1 + (gain.rolling(14).mean() / loss.rolling(14).mean())))
        
        vectors = []
        for i in range(200, len(df) - 10):
            # 1. Structural Trend: Price > 200 SMA
            if df['Close'].iloc[i] < df['SMA200'].iloc[i]: continue
            
            # 2. Alpha Gates (Exclusions)
            if df['RSI'].iloc[i] > 65: continue # RSI Ceiling
            if (df['Close'].iloc[i] / df['SMA50'].iloc[i] - 1) > 0.08: continue # SMA Stretch
            
            # 3. Institutional Signal (Volume Breakout > 130%)
            if df['Volume'].iloc[i] > (1.3 * df['VolMA20'].iloc[i]):
                # Exit Logic: 5% stop loss or 10-day trailing profit
                entry = df['Close'].iloc[i]
                stop_loss = entry * 0.95
                
                future = df.iloc[i+1 : i+11]
                hit_invalidation = False
                ret = 0
                
                # Check for thesis fulfillment
                for idx, (date, row) in enumerate(future.iterrows()):
                    if row['Low'] < stop_loss:
                        hit_invalidation = True
                        ret = -5.0 # Stop loss hit
                        break
                    # Take Profit after 10 days
                    ret = ((future.iloc[-1]['Close'] / entry) - 1) * 100
                
                vectors.append({"symbol": symbol, "date": str(df.index[i].date()), "invalidated": hit_invalidation, "return": round(ret, 2)})
        return vectors
    except: return []

results = []
for s in UNIVERSE:
    results.extend(run_precision_backtest(s))

# Calculate Success Rate
wins = [r for r in results if r['return'] > 0]
success_rate = (len(wins) / len(results)) * 100 if len(results) > 0 else 0
avg_return = sum([r['return'] for r in results]) / len(results) if len(results) > 0 else 0

output = {
    "total_vectors": len(results),
    "success_rate": round(success_rate, 2),
    "avg_return": round(avg_return, 2),
    "sample": results[:20]
}

print(json.dumps(output, indent=4))
