import sqlite3
from config import *
from datetime import datetime


def add_request(user_id, username, text, department):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute("INSERT INTO requests (user_id, username, text, department, created_at) VALUES (?, ?, ?, ?, ?)",
                   (user_id, username, text, department, created_at))
    conn.commit()
    conn.close()


def setup_database():
    conn = sqlite3.connect(DATABASE)  
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            text TEXT,
            department TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()  
setup_database()


