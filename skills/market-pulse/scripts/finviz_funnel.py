import urllib.request
import re
import sys

def get_finviz_tickers():
    # Filters: 
    # cap_smallover = Market Cap > $300M
    # sh_price_o5 = Price > $5
    # ta_unusualvolume = Unusual Volume (Spiking today)
    url = "https://finviz.com/screener.ashx?v=111&f=cap_smallover,sh_price_o5&s=ta_unusualvolume"
    
    # Finviz requires a realistic User-Agent or it throws a 403 Forbidden
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        # Finviz table links look like: quote.ashx?t=TICKER
        pattern = r'quote\.ashx\?t=([A-Z]+)'
        
        # Extract, deduplicate, and preserve order (roughly)
        seen = set()
        tickers = []
        for t in re.findall(pattern, html):
            if t not in seen:
                seen.add(t)
                tickers.append(t)
                
        return tickers[:20] # Return top 20 to keep downstream API calls safe
    except Exception as e:
        print(f"Error scraping Finviz: {e}")
        return []

if __name__ == "__main__":
    tickers = get_finviz_tickers()
    if tickers:
        print(",".join(tickers))
    else:
        print("No tickers found or scraping failed.")