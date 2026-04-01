import yfinance as yf
import pandas as pd
import numpy as np
import json

# Universe of high-growth tech/growth tickers for audit
TICKERS = ['ASTS', 'VKTX', 'RKLB', 'ZETA', 'IONQ', 'APP', 'CRWD', 'DDOG', 'MDB', 'NET', 
           'FTNT', 'PANW', 'ZS', 'OKTA', 'TTD', 'RBLX', 'DOCU', 'ZM', 'TDOC', 'PATH', 
           'ESTC', 'BILL', 'DT', 'SNOW', 'CRSP', 'EDIT', 'NTLA', 'CRBU', 'NVDA', 'AMD']

def calculate_technical_score(df):
    score = 0
    # 1. Golden Cross (50 > 200 SMA)
    sma50 = df['Close'].rolling(50).mean()
    sma200 = df['Close'].rolling(200).mean()
    if sma50.iloc[-1] > sma200.iloc[-1]: score += 3
    
    # 2. MACD (Close > 0 on signal line)
    ema12 = df['Close'].ewm(span=12).mean()
    ema26 = df['Close'].ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()
    if macd.iloc[-1] > signal.iloc[-1]: score += 3
    
    # 3. Volume Surge (> 130% of 20MA)
    vol_ma = df['Volume'].rolling(20).mean()
    if df['Volume'].iloc[-1] > (1.3 * vol_ma.iloc[-1]): score += 4
    
    return score

def get_fundamental_score(ticker):
    try:
        info = ticker.info
        score = 0
        
        # 1. PEG Ratio < 1.2
        if info.get('pegRatio', 10) < 1.2: score += 3
        
        # 2. ROE > 15%
        if info.get('returnOnEquity', 0) > 0.15: score += 4
        
        # 3. Positive Operating Margin
        if info.get('operatingMargins', 0) > 0: score += 3
        
        return score
    except:
        return 0

def run_pipeline():
    report = []
    for sym in TICKERS:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="1y")
            if len(hist) < 200: continue
            
            tech = calculate_technical_score(hist)
            fund = get_fundamental_score(ticker)
            
            if tech > 0 and fund > 0:
                report.append({
                    "ticker": sym,
                    "fundamental_score": fund,
                    "technical_score": tech,
                    "total_alpha_score": tech + fund
                })
        except:
            continue
    return sorted(report, key=lambda x: x['total_alpha_score'], reverse=True)

final_list = run_pipeline()
print(json.dumps(final_list, indent=4))
