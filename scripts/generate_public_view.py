import csv
import json
import hashlib

# Configuration
INPUT_FILE = 'PORTFOLIO_LEDGER.csv'
OUTPUT_FILE = 'dashboard_data.json'

def generate_dashboard_view():
    data = []
    
    with open(INPUT_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create a masked ID based on ticker + date for unique identification without exposing internal DB keys
            unique_id_str = f"{row['ticker']}_{row['date']}"
            masked_id = hashlib.sha256(unique_id_str.encode()).hexdigest()[:12]
            
            # Select specific public-facing fields
            public_entry = {
                'id': masked_id,
                'ticker': row['ticker'],
                'entry_price': float(row['entry_usd']),
                'current_price': float(row['current_usd']),
                'pl_pct': float(row['pl_pct']),
                'category': row['category'],
                'status': row['status']
            }
            data.append(public_entry)
            
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully generated {OUTPUT_FILE} with {len(data)} positions.")

if __name__ == '__main__':
    generate_dashboard_view()
