import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "judgments.db")

def add_tags_to_judgment(judgment_id: int, tags: list):
    """إضافة تاجات لحكم معين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # جلب التاجات الحالية
    cursor.execute("SELECT tags FROM judgments WHERE id = ?", (judgment_id,))
    result = cursor.fetchone()
    
    if result:
        current_tags = result[0].split(",") if result[0] else []
        new_tags = list(set(current_tags + tags))  # إزالة التكرار
        tags_str = ",".join(new_tags)
        
        cursor.execute("UPDATE judgments SET tags = ? WHERE id = ?", (tags_str, judgment_id))
        conn.commit()
    
    conn.close()
    return True

def get_judgment_tags(judgment_id: int):
    """جلب تاجات حكم معين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM judgments WHERE id = ?", (judgment_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0]:
        return result[0].split(",")
    return []

def search_by_tag(tag: str):
    """البحث عن أحكام تحتوي على تاج معين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM judgments 
        WHERE tags LIKE ?
        ORDER BY judgment_date DESC
    ''', (f'%{tag}%',))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_tags():
    """جلب كل التاجات الموجودة في قاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM judgments")
    all_tags = set()
    
    for row in cursor.fetchall():
        if row[0]:
            tags = row[0].split(",")
            all_tags.update(tags)
    
    conn.close()
    return sorted(list(all_tags))