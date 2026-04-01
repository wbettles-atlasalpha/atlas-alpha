import yfinance as yf
from datetime import datetime, timedelta

# Define the market scan period
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

# Scan for top 20 stocks with the largest volume spikes
def market_scan(start, end):
    tickers = yf.download('AAPL META TSLA AMZN GOOG MSFT NVDA FB BABA TSM NFLX')  # Just an example, list to be expanded
    candidates = []
    for ticker in tickers:
        data = yf.download(ticker, start=start, end=end)
        if data is not None and not data.empty:
            volume_30day_avg = data['Volume'].rolling(window=30).mean().iloc[-1]
            if data['Volume'].iloc[-1] > volume_30day_avg * 2:
                candidates.append(ticker)
    return candidates

# Perform fundamental analysis on candidates
def fundamental_analysis(candidates):
    analysis = {}
    for candidate in candidates:
        stock = yf.Ticker(candidate)
        info = stock.info
        pe_ratio = info.get('forwardPE')
        roe = info.get('returnOnEquity')
        eps_growth = info.get('earningsGrowth')

        analysis[candidate] = {
            'P/E': pe_ratio,
            'ROE': roe,
            'EPS Growth': eps_growth,
        }

    return analysis

# Run the market scan
strong_buy_candidates = market_scan(start_date, end_date)
# Run the fundamental analysis
analysis_results = fundamental_analysis(strong_buy_candidates)

print("Strong Buy Candidates: ")
print(strong_buy_candidates)
print("\nFundamental Analysis Results:")
for candidate, metrics in analysis_results.items():
    print(f"\n{candidate}: ")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")
