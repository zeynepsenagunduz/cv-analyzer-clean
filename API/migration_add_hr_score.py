# ============================================================
# MIGRATION: hr_match_score Sütunu Ekle
# Database: tez_db.sqlite
# ============================================================

import sqlite3

def add_hr_match_score():
    """applications tablosuna hr_match_score sütunu ekle"""
    
    conn = sqlite3.connect('tez_db.sqlite')  # ← tez_db.sqlite
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("MIGRATION: hr_match_score Sütunu Ekleniyor...")
    print("Database: tez_db.sqlite")
    print("="*60)
    
    try:
        # Yeni sütun ekle
        cursor.execute("""
            ALTER TABLE applications 
            ADD COLUMN hr_match_score REAL
        """)
        print("✅ hr_match_score sütunu eklendi!")
        
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("⚠️  Sütun zaten var, atlanıyor...")
        else:
            print(f"❌ Hata: {e}")
            conn.close()
            return False
    
    # Değişiklikleri kaydet
    conn.commit()
    
    # Kontrol et
    cursor.execute("PRAGMA table_info(applications)")
    columns = cursor.fetchall()
    
    print("\n" + "-"*60)
    print("applications Tablosu Sütunları:")
    print("-"*60)
    for col in columns:
        print(f"  {col[1]:<20} {col[2]}")
    
    print("\n" + "="*60)
    print("✅ Migration başarıyla tamamlandı!")
    print("="*60)
    print("\nŞimdi yapılacak:")
    print("  1. Backend'de /api/apply endpoint'ini güncelle")
    print("  2. hr_match_score değerini de kaydet")
    print("\n")
    
    conn.close()
    return True


if __name__ == "__main__":
    add_hr_match_score()
