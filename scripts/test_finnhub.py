import requests
import json

# Using the Finnhub API Key from TOOLS.md
API_KEY = "d6n9cvhr01qlnj39nfm0d6n9cvhr01qlnj39nfmg"

def get_fundamental_data(symbol):
    url = f"https://finnhub.io/api/v1/stock/financials-reported?symbol={symbol}&token={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Test call for NVDA
data = get_fundamental_data("NVDA")
if data:
    print("API Connection Successful")
    # Inspecting first entry for FCF/Revenue data structure
    print(json.dumps(data['data'][0]['report'], indent=2)[:500])
else:
    print("API Connection Failed")
