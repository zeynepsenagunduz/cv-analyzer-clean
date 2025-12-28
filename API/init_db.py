#!/usr/bin/env python3
"""
Veritabanını başlatır ve örnek verileri yükler
"""
from db import init_database, get_db_connection
from utils.jobpostToDatabase import jobpostToDatabase
from add_courses import courses_data
import os

def add_courses_to_db():
    """Kursları veritabanına ekler"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Mevcut kurs sayısını kontrol et
    cursor.execute("SELECT COUNT(*) FROM courses")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"Veritabanında zaten {existing_count} kurs var. Kurslar atlanıyor...")
        conn.close()
        return
    
    added_count = 0
    for course in courses_data:
        try:
            cursor.execute(
                "INSERT INTO courses (name, keywords, link) VALUES (?, ?, ?)",
                (course["name"], course["keywords"], course["link"])
            )
            added_count += 1
        except Exception as e:
            print(f"Hata ({course['name']}): {e}")
    
    conn.commit()
    conn.close()
    print(f"{added_count} kurs eklendi.")

def main():
    print("Veritabanı başlatılıyor...")
    init_database()
    
    print("\nKurslar yükleniyor...")
    add_courses_to_db()
    
    print("\nJobpost verileri yükleniyor...")
    jobpostToDatabase()
    
    print("\n✓ Veritabanı hazır!")

if __name__ == "__main__":
    main()

