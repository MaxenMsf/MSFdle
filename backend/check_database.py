#!/usr/bin/env python3
"""
Vérification de la structure de la base de données
"""
import sqlite3

def check_database():
    conn = sqlite3.connect('../data/msfdle.db')
    cursor = conn.cursor()
    
    print("🗄️ Structure de la base de données")
    print("=" * 50)
    
    # Lister toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("📋 Tables disponibles:")
    for table in tables:
        print(f"   - {table[0]}")
    
    print()
    
    # Vérifier les colonnes de chaque table
    for table in tables:
        table_name = table[0]
        print(f"📊 Structure de '{table_name}':")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_database()