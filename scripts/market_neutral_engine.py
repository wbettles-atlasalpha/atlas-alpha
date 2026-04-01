import yfinance as yf
import pandas as pd
import json

# Dow Jones 30 Universe (Sample)
SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GS", "JPM", "JNJ", "PG", "HD", "CVX", "MRK", "KO", "PEP", "BAC"]

def run_neutral_backtest(symbol):
    try:
        df = yf.Ticker(symbol).history(period="10y")
        if len(df) < 250: return []
        
        df['VolMA20'] = df['Volume'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = delta.clip(upper=0).abs()
        rsi = 100 - (100 / (1 + (gain.rolling(14).mean() / loss.rolling(14).mean())))
        
        vectors = []
        for i in range(200, len(df) - 10):
            # LONG SIDE (Accumulation)
            # Price > SMA200 + Volume Breakout UP + RSI < 65 (Not overbought)
            if df['Close'].iloc[i] > df['SMA200'].iloc[i] and rsi.iloc[i] < 65:
                if df['Volume'].iloc[i] > (1.2 * df['VolMA20'].iloc[i]):
                    ret = ((df['Close'].iloc[i+10] / df['Close'].iloc[i]) - 1) * 100
                    vectors.append({"side": "LONG", "symbol": symbol, "return": round(ret, 2)})
            
            # SHORT SIDE (Distribution)
            # Price < SMA50 + Volume Breakout DOWN + RSI < 40 (Weakness)
            elif df['Close'].iloc[i] < df['SMA50'].iloc[i] and rsi.iloc[i] < 40:
                if df['Volume'].iloc[i] > (1.2 * df['VolMA20'].iloc[i]):
                    ret = ((df['Close'].iloc[i] / df['Close'].iloc[i+10]) - 1) * 100 # Short return
                    vectors.append({"side": "SHORT", "symbol": symbol, "return": round(ret, 2)})
                    
        return vectors
    except: return []

final_report = []
for s in SYMBOLS:
    final_report.extend(run_neutral_backtest(s))

print(json.dumps(final_report, indent=4))
