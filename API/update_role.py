#!/usr/bin/env python3
"""
Kullanıcının role değerini günceller
"""
from db import get_db_connection
import sys

def update_user_role(userid, new_role):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Mevcut değeri kontrol et
    cursor.execute("SELECT id, username, role FROM users WHERE id=?", (userid,))
    user = cursor.fetchone()
    
    if not user:
        print(f"Kullanıcı ID={userid} bulunamadı!")
        conn.close()
        return
    
    print(f"Mevcut değerler:")
    print(f"  ID: {user[0]}")
    print(f"  Username: {user[1]}")
    print(f"  Role: {user[2]} (Type: {type(user[2])})")
    
    # Role değerini güncelle
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (str(new_role), userid))
    conn.commit()
    
    # Güncellenmiş değeri kontrol et
    cursor.execute("SELECT id, username, role FROM users WHERE id=?", (userid,))
    updated_user = cursor.fetchone()
    
    print(f"\nGüncellenmiş değerler:")
    print(f"  ID: {updated_user[0]}")
    print(f"  Username: {updated_user[1]}")
    print(f"  Role: {updated_user[2]} (Type: {type(updated_user[2])})")
    
    conn.close()
    print(f"\n✓ Role değeri başarıyla güncellendi!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python3 update_role.py <userid> <new_role>")
        print("Örnek: python3 update_role.py 2 1")
        sys.exit(1)
    
    userid = int(sys.argv[1])
    new_role = sys.argv[2]  # String olarak al, çünkü TEXT olarak saklanıyor
    update_user_role(userid, new_role)

