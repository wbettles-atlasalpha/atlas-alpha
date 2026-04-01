import sys
import os
import json
import time
import urllib.request
from urllib.error import URLError
from datetime import datetime, timedelta

def get_finnhub_news(ticker, api_key):
    if not api_key:
        return ""
    
    # Get dates for the last 3 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={start_date}&to={end_date}&token={api_key}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            news_data = json.loads(response.read().decode())
            
        if news_data and len(news_data) > 0:
            # Get top 2 most recent headlines
            headlines = [item['headline'] for item in news_data[:2] if 'headline' in item]
            if headlines:
                return f"\n      └─ 🗞️ Catalyst: {headlines[0]}" + (f"\n      └─ 🗞️ Catalyst: {headlines[1]}" if len(headlines) > 1 else "")
    except Exception as e:
        pass
    return "\n      └─ 🗞️ Catalyst: No major news in last 72 hours."

def get_volume_spikes(tickers_list, threshold, alpha_key, finnhub_key):
    tickers = [t.strip().upper() for t in tickers_list.split(",")]
    spikes = []
    
    for ticker in tickers:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={alpha_key}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
            if "Time Series (Daily)" not in data:
                continue
                
            time_series = data["Time Series (Daily)"]
            dates = sorted(time_series.keys(), reverse=True)
            
            if len(dates) < 11:
                continue
                
            recent_dates = dates[:11]
            
            current_date = recent_dates[0]
            current_volume = float(time_series[current_date]["5. volume"])
            current_close = float(time_series[current_date]["4. close"])
            
            prev_close = float(time_series[recent_dates[1]]["4. close"])
            change = ((current_close - prev_close) / prev_close) * 100
            
            past_10_volumes = [float(time_series[d]["5. volume"]) for d in recent_dates[1:11]]
            avg_volume = sum(past_10_volumes) / 10
            
            if avg_volume == 0:
                continue
                
            volume_ratio = current_volume / avg_volume
            
            if volume_ratio >= threshold:
                status = "🔥 SPIKE" if volume_ratio > 2 else "📈 ELEVATED"
                news_context = get_finnhub_news(ticker, finnhub_key)
                
                spikes.append(
                    f"{ticker:<5} | Price: ${current_close:<7.2f} | Change: {change:>5.2f}% | Vol Ratio: {volume_ratio:<5.2f}x | {status}{news_context}"
                )
        except Exception as e:
            pass
            
        # Respect Finnhub & Alpha Vantage free tier rate limits (max 60/min)
        time.sleep(1.2)
            
    if not spikes:
        return "No significant volume spikes detected in the current watchlist."
        
    header = f"{'SYM':<5} | {'Price':<14} | {'Change':<13} | {'Vol Ratio':<17} | Status & Catalyst\n"
    header += "-" * 90
    return header + "\n" + "\n".join(spikes)

if __name__ == "__main__":
    alpha_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    finnhub_key = os.environ.get("FINNHUB_API_KEY")
    
    if not alpha_key:
        print("Error: ALPHAVANTAGE_API_KEY environment variable is missing.")
        sys.exit(1)
        
    tickers = sys.argv[1] if len(sys.argv) > 1 else "AAPL,TSLA,NVDA,AMD,MSFT"
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
    print(get_volume_spikes(tickers, threshold, alpha_key, finnhub_key))