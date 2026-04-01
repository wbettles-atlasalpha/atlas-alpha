import yfinance as yf
import pandas as pd
import json
import logging

# Atlas Alpha: Precision Mid-Cap Drift Scan
# Focus: Market Cap $2B - $500B. 
# Avoids retail-crowded mega-caps and illiquid micro-caps.

logging.basicConfig(level=logging.ERROR)

def get_tickers():
    try:
        with open('/home/warwick/.openclaw/workspace/data/tickers.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load tickers: {e}")
        return []

def scan_drift():
    valid_signals = []
    tickers = get_tickers()
    print(f"Starting Precision Mid-Cap Drift Scan: {len(tickers)} tickers...")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            
            # Fundamental Filters: Market Cap & Volume
            info = ticker.info
            mkt_cap = info.get('marketCap', 0)
            avg_vol = info.get('averageVolume', 0)
            
            # Sweet spot: $2B to $500B, Vol > 500k
            if not (2e9 < mkt_cap < 500e9) or avg_vol < 500000:
                continue
            
            hist = ticker.history(period="1mo")
            if len(hist) < 20: 
                continue
            
            # Scan last 15 days
            for i in range(1, len(hist)):
                prev = hist.iloc[i-1]
                curr = hist.iloc[i]
                
                # Gap > 5%
                if ((curr['Close'] - prev['Close']) / prev['Close']) > 0.05:
                    entry = curr['Close']
                    gap_fill = entry * 0.95
                    
                    # 10-day stability test
                    window = hist.iloc[i+1 : min(i+11, len(hist))]
                    if len(window) >= 5 and all(window['Low'] >= gap_fill):
                        valid_signals.append({
                            "symbol": symbol,
                            "entry": round(entry, 2),
                            "date": curr.name.strftime('%Y-%m-%d'),
                            "mkt_cap": mkt_cap
                        })
                        break 
        except Exception:
            continue
    
    with open('/home/warwick/.openclaw/workspace/MARKET_SCAN_RESULTS.json', 'w') as f:
        json.dump(valid_signals, f)
    print(f"Scan complete. Found {len(valid_signals)} signals.")

if __name__ == "__main__":
    scan_drift()
