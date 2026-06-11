import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "judgments.db")

def init_db():
    """إنشاء قاعدة البيانات وجدول الأحكام"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS judgments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_number TEXT NOT NULL,
            court TEXT NOT NULL,
            judgment_date TEXT NOT NULL,
            ruling TEXT NOT NULL,
            summary TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ قاعدة بيانات الأحكام جاهزة")

def add_judgment(case_number: str, court: str, judgment_date: str, ruling: str, summary: str = "", tags: str = ""):
    """إضافة حكم جديد إلى قاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO judgments (case_number, court, judgment_date, ruling, summary, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (case_number, court, judgment_date, ruling, summary, tags))
    conn.commit()
    conn.close()
    return True

def search_judgments(query: str):
    """البحث في الأحكام"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM judgments 
        WHERE case_number LIKE ? 
           OR court LIKE ? 
           OR ruling LIKE ? 
           OR tags LIKE ?
        ORDER BY judgment_date DESC
    ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_judgments():
    """جلب كل الأحكام"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM judgments ORDER BY judgment_date DESC')
    results = cursor.fetchall()
    conn.close()
    return results

# تشغيل التهيئة عند استيراد الملف
init_db()