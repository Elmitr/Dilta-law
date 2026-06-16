import sqlite3
import os
from typing import List, Dict

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "judgments.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS library_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            item_type TEXT,
            description TEXT,
            file_path TEXT,
            tags TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_library_item(title: str, item_type: str, description: str = "", 
                     file_path: str = "", tags: str = "") -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO library_items (title, item_type, description, file_path, tags)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, item_type, description, file_path, tags))
    
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def get_all_library_items() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM library_items ORDER BY uploaded_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    columns = ['id', 'title', 'item_type', 'description', 'file_path', 'tags', 'uploaded_at']
    return [dict(zip(columns, row)) for row in rows]
