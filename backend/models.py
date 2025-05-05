import sqlite3
from contextlib import contextmanager
import os

DB_PATH = os.environ.get('DATABASE_URL', 'leads.db').replace('sqlite:///', '')

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                category TEXT,
                address TEXT,
                website TEXT,
                status TEXT DEFAULT 'Not Called',
                buyer_count INTEGER DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS call_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                call_status TEXT,
                transcript TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        conn.commit()
        
        # Check if buyer_count column exists and add it if not
        try:
            conn.execute('SELECT buyer_count FROM leads LIMIT 1')
        except sqlite3.OperationalError:
            # Column doesn't exist, add it
            conn.execute('ALTER TABLE leads ADD COLUMN buyer_count INTEGER DEFAULT 0')
            conn.commit()
