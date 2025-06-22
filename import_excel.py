import pandas as pd
import argparse
from db import init_db, add_or_update_title

def import_excel(file):
    init_db()
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        record = {
            'stock_number': str(row['Stock Number']),
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
    print("Import complete.")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Import titles from Excel to database.')
    parser.add_argument('file', help='Path to the Excel file')
    args = parser.parse_args()
    import_excel(args.file)
