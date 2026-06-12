import sqlite3
import os
from datetime import datetime
from typing import List, Dict

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "judgments.db")

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for judgments / legal documents
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS judgments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_number TEXT,
            court TEXT,
            judgment_date TEXT,
            ruling TEXT,
            summary TEXT,
            tags TEXT,
            source_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for legal library items
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
    print("Database initialized successfully.")

def add_library_item(title: str, item_type: str, description: str = "", 
                     file_path: str = "", tags: str = "") -> int:
    """Add a new item to the legal library."""
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
    """Get all items in the legal library."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM library_items ORDER BY uploaded_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    columns = ['id', 'title', 'item_type', 'description', 'file_path', 'tags', 'uploaded_at']
    return [dict(zip(columns, row)) for row in rows]

if __name__ == "__main__":
    init_db()
