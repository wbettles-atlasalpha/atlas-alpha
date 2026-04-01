import urllib.request
import xml.etree.ElementTree as ET
import re
import sys

def get_reddit_leads():
    subs = ['stocks', 'investing', 'ASX_Bets']
    # Custom User-Agent prevents Reddit from blocking the request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AtlasAlphaBot/1.0'}
    
    # Filter out common capitalized words that aren't stock tickers
    ignore_list = {'THE', 'AND', 'FOR', 'ARE', 'YOU', 'HOW', 'WHY', 'WHAT', 'ETF', 'FED', 'CEO', 'CFO', 'EPS', 'YOY', 'IPO', 'SEC', 'WSB', 'NYSE', 'NASDAQ', 'USA', 'FOMC', 'DCA', 'IRA', 'YTD', 'AI', 'TECH', 'ALL', 'OUT', 'NEW', 'NOW', 'BUY', 'SELL', 'HOLD'}
    
    leads = []
    
    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/new.rss"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            # Check the 15 newest posts per subreddit
            for entry in root.findall('atom:entry', ns)[:15]: 
                title = entry.find('atom:title', ns).text
                link = entry.find('atom:link', ns).attrib['href']
                
                # Look for cashtags or isolated uppercase words (2-5 letters)
                potential_tickers = re.findall(r'\b[A-Z]{2,5}\b', title)
                cash_tags = re.findall(r'\$[A-Za-z]{2,5}\b', title)
                
                found_tickers = set()
                for pt in potential_tickers:
                    if pt not in ignore_list:
                        found_tickers.add(pt)
                for ct in cash_tags:
                    found_tickers.add(ct.replace('$', '').upper())
                    
                if found_tickers:
                    leads.append({
                        'sub': sub,
                        'title': title,
                        'link': link,
                        'tickers': list(found_tickers)
                    })
                    
        except Exception as e:
            pass # Silently skip subreddits if rate limited momentarily
            
    return leads

if __name__ == "__main__":
    leads = get_reddit_leads()
    if not leads:
        print("No actionable ticker mentions found in the last hour.")
    else:
        print("🎯 ATLAS ALPHA: REDDIT SNIPER LEADS 🎯\n")
        # Just show the top 5 to avoid overwhelming the daily brief
        for lead in leads[:5]:
            print(f"Subreddit : r/{lead['sub']}")
            print(f"Title     : {lead['title']}")
            print(f"Tickers   : {', '.join(lead['tickers'])}")
            print(f"Link      : {lead['link']}")
            print("-" * 60)