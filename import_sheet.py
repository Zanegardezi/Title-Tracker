import pandas as pd
import argparse
from db import init_db, add_or_update_title

def import_sheet(sheet_url):
    match = __import__('re').search(r'/d/([^/]+)', sheet_url)
    if not match:
        print("Invalid Google Sheet URL.")
        return
    sheet_id = match.group(1)
    gid_match = __import__('re').search(r'gid=(\d+)', sheet_url)
    gid = gid_match.group(1) if gid_match else '0'
    csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
    df = pd.read_csv(csv_url)
    init_db()
    for _, row in df.iterrows():
        record = {
            'stock_number': str(row.get('Stock Number','')).strip(),
            'vin': str(row.get('VIN','') or ''),
            'check_status': row.get('Check Status',''),
            'check_number': str(row.get('Check Number','')),
            'handled_by': row.get('Handled by',''),
            'status': row.get('Status',''),
            'title_received_date': pd.to_datetime(row.get('Title received date')).isoformat(sep=' ', timespec='seconds') if pd.notnull(row.get('Title received date')) else '',
            'check_sent_date': pd.to_datetime(row.get('Check sent date')).isoformat(sep=' ', timespec='seconds') if pd.notnull(row.get('Check sent date')) else '',
            'lien_holder': row.get('Lien Holder',''),
            'unit_status': row.get('Unit Status',''),
            'notes': row.get('Notes',''),
        }
        add_or_update_title(record)
    print("Import from Google Sheet complete.")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Import titles directly from Google Sheets URL.')
    parser.add_argument('sheet_url', help='Full URL of the Google Sheet')
    args = parser.parse_args()
    import_sheet(args.sheet_url)
