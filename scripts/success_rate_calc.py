import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def analyze_success_rate(tickers, start_date, end_date):
    results = []
    for ticker_symbol in tickers:
        try:
            ticker = yf.Ticker(ticker_symbol)
            df = ticker.history(start=start_date, end=end_date)
            if len(df) < 20: continue
            df['PrevClose'] = df['Close'].shift(1)
            df['Gap'] = (df['Open'] - df['PrevClose']) / df['PrevClose']
            gap_ups = df[df['Gap'] > 0.05]
            for idx, row in gap_ups.iterrows():
                entry_price = row['Open']
                stop_loss = entry_price * 0.95
                date_idx = df.index.get_loc(idx)
                if date_idx + 15 >= len(df): continue
                stability_window = df.iloc[date_idx + 1 : date_idx + 11]
                if (stability_window['Low'] < stop_loss).any(): continue
                exit_price = df.iloc[date_idx + 15]['Close']
                performance = (exit_price - entry_price) / entry_price
                results.append(performance)
        except Exception: continue
    return results

ftse_100_tickers = [
    'AAL.L', 'ABDN.L', 'ABF.L', 'ADM.L', 'AHT.L', 'ANTO.L', 'AUTO.L', 'AV.L', 'AZN.L', 'BA.L',
    'BARC.L', 'BATS.L', 'BDEV.L', 'BLND.L', 'BP.L', 'BRBY.L', 'BRLA.L', 'BT-A.L', 'CCH.L', 'CPG.L',
    'CRDA.L', 'CRH.L', 'DCC.L', 'DGE.L', 'DLN.L', 'ENT.L', 'EXPN.L', 'FLTR.L', 'FRAS.L', 'GLEN.L',
    'GSK.L', 'HL.L', 'HLMA.L', 'HMSO.L', 'HSBA.L', 'HTG.L', 'IAG.L', 'III.L', 'IMB.L', 'INVP.L',
    'ITRK.L', 'JD.L', 'JE.L', 'KGF.L', 'LAND.L', 'LGEN.L', 'LLOY.L', 'LSEG.L', 'MNG.L', 'MRO.L',
    'NG.L', 'NXT.L', 'PHNX.L', 'PRU.L', 'PSN.L', 'REL.L', 'RIO.L', 'RMV.L', 'RR.L', 'RTO.L',
    'SAGE.L', 'SBRY.L', 'SDR.L', 'SGRO.L', 'SHEL.L', 'SKG.L', 'SMDS.L', 'SMIN.L', 'SN.L', 'SSE.L',
    'STAN.L', 'STJ.L', 'SVS.L', 'SXR.L', 'TW.L', 'ULVR.L', 'UU.L', 'VOD.L', 'WTB.L', 'WPP.L'
]
end = datetime.now()
start = end - timedelta(days=365)
returns = analyze_success_rate(ftse_100_tickers, start, end)
success_rate = sum(1 for r in returns if r > 0) / len(returns) if returns else 0
print(f"Success Rate: {success_rate:.2%}")
