import sqlite3
from datetime import datetime

DB_NAME = 'titles.db'

def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS titles (
            stock_number TEXT PRIMARY KEY,
            vin TEXT,
            check_status TEXT,
            check_number TEXT,
            handled_by TEXT,
            status TEXT,
            title_received_date TEXT,
            check_sent_date TEXT,
            lien_holder TEXT,
            unit_status TEXT,
            notes TEXT
        )""")
    c.execute("""CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_number TEXT,
            old_status TEXT,
            new_status TEXT,
            timestamp TEXT
        )""")
    conn.commit()
    conn.close()

def add_or_update_title(record):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT status FROM titles WHERE stock_number=?', (record['stock_number'],))
    row = c.fetchone()
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    if row:
        old_status = row['status']
        c.execute(
            """UPDATE titles
            SET vin=?, check_status=?, check_number=?, handled_by=?, status=?, title_received_date=?, check_sent_date=?, lien_holder=?, unit_status=?, notes=?
            WHERE stock_number=?""",
            (
                record['vin'], record['check_status'], record['check_number'], record['handled_by'],
                record['status'], record['title_received_date'], record['check_sent_date'],
                record['lien_holder'], record['unit_status'], record['notes'], record['stock_number']
            )
        )
        new_status = record['status']
        if old_status != new_status:
            c.execute(
                'INSERT INTO history (stock_number, old_status, new_status, timestamp) VALUES (?,?,?,?)',
                (record['stock_number'], old_status, new_status, timestamp)
            )
    else:
        c.execute(
            'INSERT INTO titles (stock_number, vin, check_status, check_number, handled_by, status, title_received_date, check_sent_date, lien_holder, unit_status, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            (
                record['stock_number'], record['vin'], record['check_status'], record['check_number'],
                record['handled_by'], record['status'], record['title_received_date'],
                record['check_sent_date'], record['lien_holder'], record['unit_status'], record['notes']
            )
        )
    conn.commit()
    conn.close()

def get_active_titles():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM titles WHERE status!='Title received'")
    rows = c.fetchall()
    conn.close()
    return rows

def get_archived_titles():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM titles WHERE status='Title received'")
    rows = c.fetchall()
    conn.close()
    return rows

def mark_received(stock_numbers):
    conn = get_conn()
    c = conn.cursor()
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    for sn in stock_numbers:
        c.execute('SELECT status FROM titles WHERE stock_number=?', (sn,))
        row = c.fetchone()
        if row and row['status'] != 'Title received':
            old_status = row['status']
            c.execute(
                "UPDATE titles SET status=?, title_received_date=? WHERE stock_number=?",
                ('Title received', timestamp, sn)
            )
            c.execute(
                'INSERT INTO history (stock_number, old_status, new_status, timestamp) VALUES (?,?,?,?)',
                (sn, old_status, 'Title received', timestamp)
            )
    conn.commit()
    conn.close()

def get_history(stock_number):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM history WHERE stock_number=? ORDER BY timestamp', (stock_number,))
    rows = c.fetchall()
    conn.close()
    return rows
