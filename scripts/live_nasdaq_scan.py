import yfinance as yf
import pandas as pd
import json

# Nasdaq-100 Tickers
NASDAQ_100 = [
    "AAPL", "MSFT", "AMZN", "NVDA", "META", "GOOGL", "AVGO", "TSLA", "COST", "PEP",
    "ADBE", "AMD", "NFLX", "INTC", "CSCO", "CMCSA", "AMGN", "HON", "TXN", "QCOM",
    "TMUS", "INTU", "SBUX", "GILD", "MDLZ", "BKNG", "ADP", "VRTX", "MU", "REGN",
    "LRCX", "ADI", "KLAC", "SNPS", "CDNS", "ASML", "CSGP", "DXCM", "PAYX", "PYPL"
]

def scan_live_vectors():
    vectors = []
    for sym in NASDAQ_100:
        try:
            df = yf.Ticker(sym).history(period="1y")
            if len(df) < 200: continue
            
            df['VolMA20'] = df['Volume'].rolling(20).mean()
            df['SMA200'] = df['Close'].rolling(200).mean()
            df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
            
            # The "Parity & Stability" Logic
            # 1. Structural Trend: Price > 200 SMA
            # 2. Volume Parity: Current vol is 0.95 - 1.05 of 20MA
            # 3. Stability: ATR / Price is 0.02 - 0.04 (approx 3%)
            
            curr = df.iloc[-1]
            vol_parity = curr['Volume'] / df['VolMA20'].iloc[-1]
            atr_ratio = df['ATR14'].iloc[-1] / curr['Close']
            
            if curr['Close'] > df['SMA200'].iloc[-1]:
                if 0.95 <= vol_parity <= 1.05:
                    if 0.02 <= atr_ratio <= 0.04:
                        vectors.append({
                            "symbol": sym, 
                            "price": round(curr['Close'], 2),
                            "vol_parity": round(vol_parity, 2),
                            "atr_ratio": round(atr_ratio, 3)
                        })
        except: continue
    return vectors

print(json.dumps(scan_live_vectors(), indent=4))
