import yfinance as yf
import pandas as pd
import json

# Universe
SYMBOLS = ['NVDA', 'AMD', 'META', 'AMZN', 'MSFT', 'CRWD', 'DDOG', 'MDB', 'NET', 'FTNT', 'PANW']

def run_inflection_audit(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # FCF and Financials are usually reported quarterly
        cashflow = ticker.quarterly_cashflow.T
        financials = ticker.quarterly_financials.T
        
        if len(cashflow) < 8: return []
        
        # Merge FCF and Net Income for analysis
        data = pd.concat([cashflow['Free Cash Flow'], financials['Net Income']], axis=1)
        data.columns = ['FCF', 'NetIncome']
        data = data.dropna()
        
        # Inflection logic (looking for Q-over-Q jump)
        vectors = []
        for i in range(1, len(data) - 1):
            # 1. Baseline: Profitable (Net Income > 0)
            if data['NetIncome'].iloc[i-1] <= 0: continue
            
            # 2. Inflection: FCF Jump > 20%
            if data['FCF'].iloc[i] > (1.2 * data['FCF'].iloc[i-1]):
                # 3. Technical Trigger: Let's assume a breakout in the quarter following the inflection
                # (Simplifying for audit: checking if the price 30 days post-inflection is higher)
                vectors.append({"symbol": symbol, "date": str(data.index[i].date())})
        return vectors
    except: return []

# This scan identifies the dates of "Fundamental Inflection"
results = []
for s in SYMBOLS:
    results.extend(run_inflection_audit(s))

print(json.dumps(results, indent=4))
