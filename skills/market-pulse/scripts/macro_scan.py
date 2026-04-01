import sys
import os
import json
import urllib.request
from datetime import datetime, timedelta

# FRED Series IDs
# DFF = Federal Funds Effective Rate
# T10Y2Y = 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity (Yield Curve)
# WM2NS = M2 Money Supply

def get_fred_latest(series_id, api_key):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&sort_order=desc&limit=2"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if 'observations' in data and len(data['observations']) > 0:
            obs = data['observations'][0]
            val = float(obs['value']) if obs['value'] != '.' else 0.0
            date = obs['date']
            
            # Trend context
            if len(data['observations']) > 1:
                prev_obs = data['observations'][1]
                prev_val = float(prev_obs['value']) if prev_obs['value'] != '.' else 0.0
                trend = "▲" if val > prev_val else ("▼" if val < prev_val else "▶")
            else:
                trend = "▶"
                
            return val, date, trend
    except Exception as e:
        return None, None, "?"

def run_macro_pulse(api_key):
    output = []
    output.append("==================================================================")
    output.append("                 ATLAS ALPHA: GLOBAL MACRO PULSE                  ")
    output.append("==================================================================")
    
    # 1. Federal Funds Rate (Cost of Capital)
    dff_val, dff_date, dff_trend = get_fred_latest('DFF', api_key)
    if dff_val is not None:
        output.append(f"[DFF]    Federal Funds Rate : {dff_val:.2f}% {dff_trend} (As of {dff_date})")
        
    # 2. Yield Curve (Recession Indicator)
    yc_val, yc_date, yc_trend = get_fred_latest('T10Y2Y', api_key)
    if yc_val is not None:
        status = "INVERTED ⚠️" if yc_val < 0 else "NORMAL 📈"
        output.append(f"[T10Y2Y] 10Y-2Y Yield Curve : {yc_val:.2f}% {yc_trend} (As of {yc_date}) -> {status}")
        
    # 3. M2 Money Supply (Liquidity)
    m2_val, m2_date, m2_trend = get_fred_latest('WM2NS', api_key)
    if m2_val is not None:
        output.append(f"[WM2NS]  M2 Money Supply    : ${m2_val:.1f}B {m2_trend} (As of {m2_date})")

    # 4. Credit Market Canary (High Yield Spread)
    hy_val, hy_date, hy_trend = get_fred_latest('BAMLC0A0CM', api_key)
    if hy_val is not None:
        status = "HIGH STRESS 🚨" if hy_val > 5.0 else "NORMAL 🟢" if hy_val < 4.0 else "ELEVATED ⚠️"
        output.append(f"[HY_OAS] High Yield Spread  : {hy_val:.2f}% {hy_trend} (As of {hy_date}) -> {status}")

    output.append("==================================================================")
    return "\n".join(output)

if __name__ == "__main__":
    fred_key = os.environ.get("FRED_API_KEY")
    if not fred_key:
        print("Error: FRED_API_KEY environment variable is missing.")
        sys.exit(1)
        
    print(run_macro_pulse(fred_key))