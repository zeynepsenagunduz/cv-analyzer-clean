#!/usr/bin/env python3
"""
Veritabanındaki kullanıcı verilerini kontrol eder
"""
from db import get_db_connection

def check_user(userid):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tüm kullanıcıları listele
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    print("=== TÜM KULLANICILAR ===")
    for user in all_users:
        print(f"ID: {user[0]}, Username: {user[1]}, Role (index 4): {user[4]}, Role (by name): {user['role'] if hasattr(user, 'keys') else 'N/A'}")
    
    # Belirli bir kullanıcıyı kontrol et
    cursor.execute("SELECT * FROM users WHERE id=?", (userid,))
    user = cursor.fetchone()
    
    if user:
        print(f"\n=== KULLANICI ID={userid} ===")
        print(f"Full row as dict: {dict(user)}")
        print(f"Index 0 (id): {user[0]}")
        print(f"Index 1 (username): {user[1]}")
        print(f"Index 2 (email): {user[2]}")
        print(f"Index 3 (password): {user[3]}")
        print(f"Index 4 (role): {user[4]} (Type: {type(user[4])})")
        print(f"Index 5 (has_cv): {user[5]}")
        print(f"Index 6 (has_jobpost): {user[6]}")
        print(f"Index 7 (credit): {user[7] if len(user) > 7 else 'N/A'}")
        
        # Sütun isimleriyle erişim
        try:
            print(f"\nBy column name:")
            print(f"id: {user['id']}")
            print(f"username: {user['username']}") 
            print(f"email: {user['email']}")
            print(f"role: {user['role']} (Type: {type(user['role'])})")
            print(f"has_cv: {user['has_cv']}")
            print(f"has_jobpost: {user['has_jobpost']}")
        except Exception as e:
            print(f"Error accessing by column name: {e}")
    else:
        print(f"Kullanıcı ID={userid} bulunamadı!")
    
    conn.close()

if __name__ == "__main__":
    import sys
    userid = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    check_user(userid)

