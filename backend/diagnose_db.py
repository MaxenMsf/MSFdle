#!/usr/bin/env python3
"""
Script de diagnostic pour voir exactement ce qui se passe
"""

import sqlite3
import csv
import os

def diagnose_database():
    # Chemins des fichiers
    csv_path = os.path.join("..", "data", "perso.csv")
    db_path = os.path.join("..", "data", "msfdle.db")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 Diagnostic de la base de données")
    print("=" * 40)
    
    # Compter les personnages dans la base
    cursor.execute("SELECT COUNT(*) FROM characters")
    db_count = cursor.fetchone()[0]
    print(f"📊 Personnages dans la base: {db_count}")
    
    # Compter les personnages dans le CSV
    csv_count = 0
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_count = sum(1 for row in reader)
    print(f"📊 Personnages dans le CSV: {csv_count}")
    
    # Vérifier si Professeur Xavier est dans la base
    cursor.execute("SELECT * FROM characters WHERE character_id = 'Xavier' OR alias LIKE '%Xavier%'")
    xavier_results = cursor.fetchall()
    
    print(f"\n🔍 Recherche Professeur Xavier:")
    if xavier_results:
        for result in xavier_results:
            print(f"   ✅ Trouvé: {result}")
    else:
        print("   ❌ Professeur Xavier non trouvé dans la base")
    
    # Vérifier les derniers personnages dans la base
    cursor.execute("SELECT character_id, alias FROM characters ORDER BY rowid DESC LIMIT 5")
    last_chars = cursor.fetchall()
    print(f"\n📋 Derniers personnages dans la base:")
    for char in last_chars:
        print(f"   • {char[0]} - {char[1]}")
    
    # Vérifier si le CSV contient Xavier
    print(f"\n📋 Recherche Xavier dans le CSV:")
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'Xavier' in row['Character Id'] or 'Xavier' in row['Alias']:
                print(f"   ✅ Trouvé dans CSV: {row['Character Id']} - {row['Alias']} - {row['Role']}")
    
    conn.close()

if __name__ == "__main__":
    diagnose_database()