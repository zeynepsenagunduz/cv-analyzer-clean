import sqlite3
import os

DB_PATH = "tez_db.sqlite"

def get_db_connection():
    """SQLite veritabanı bağlantısı oluşturur"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Sözlük benzeri erişim için
    return conn

def init_database():
    """Veritabanı şemasını oluşturur"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # users tablosu
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
    
    # cvs tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER NOT NULL,
            keywords TEXT NOT NULL,
            FOREIGN KEY (userid) REFERENCES users(id)
        )
    ''')
    
    # jobposts tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobposts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER NOT NULL,
            jobpost TEXT NOT NULL,
            jobpost_keywords TEXT NOT NULL,
            FOREIGN KEY (userid) REFERENCES users(id)
        )
    ''')
    
    # courses tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            keywords TEXT NOT NULL,
            link TEXT NOT NULL
        )
    ''')
    
    # invitecodes tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invitecodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            used INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Veritabanı şeması oluşturuldu.")

