import sqlite3
import os

DB_PATH = "tez_db.sqlite"

def get_db_connection():
    """SQLite veritabanı bağlantısı oluşturur"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Sözlük benzeri erişim için
    return conn

def init_database():
    """Veritabanı şemasını oluşturur ve tabloları günceller"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. users tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            has_cv INTEGER DEFAULT 0,
            has_jobpost INTEGER DEFAULT 0,
            credit INTEGER DEFAULT 0
        )
    ''')
    
    # 2. cvs tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER NOT NULL,
            keywords TEXT NOT NULL,
            FOREIGN KEY (userid) REFERENCES users(id)
        )
    ''')
    
    # 3. jobposts tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobposts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER NOT NULL,
            jobpost TEXT NOT NULL,
            jobpost_keywords TEXT NOT NULL,
            FOREIGN KEY (userid) REFERENCES users(id)
        )
    ''')

    # 4. applications tablosu (fast.py'daki yeni yapıya göre)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL,
            jobpostid INTEGER NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            match_score REAL,
            hr_match_score REAL,
            cover_letter TEXT,
            FOREIGN KEY (userid) REFERENCES users(id),
            FOREIGN KEY (jobpostid) REFERENCES jobposts(id)
        )
    ''')
    
    # 5. courses tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            keywords TEXT NOT NULL,
            link TEXT NOT NULL
        )
    ''')
    
    # 6. invitecodes tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invitecodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            used INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Veritabanı şeması başarıyla güncellendi.")

if __name__ == "__main__":
    init_database()