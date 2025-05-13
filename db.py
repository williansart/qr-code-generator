import sqlite3
from datetime import datetime

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS qrcodes (
            id TEXT PRIMARY KEY,
            content TEXT,
            image_path TEXT,
            scans INTEGER DEFAULT 0,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_qr_entry(db_path, qr_id, content, image_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO qrcodes (id, content, image_path, created_at)
        VALUES (?, ?, ?, ?)
    ''', (qr_id, content, image_path, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, content, image_path, scans FROM qrcodes ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows
