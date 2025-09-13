#!/usr/bin/env python3
"""
Vérification des tags appliqués
"""
import sqlite3

def check_tags():
    conn = sqlite3.connect('../data/msfdle.db')
    cursor = conn.cursor()
    
    print("🏷️ Vérification des tags appliqués")
    print("=" * 50)
    
    # Compter les personnages avec et sans tags
    cursor.execute("SELECT COUNT(*) FROM characters WHERE tags != 'AUCUN'")
    with_tags = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM characters WHERE tags = 'AUCUN'")
    without_tags = cursor.fetchone()[0]
    
    print(f"📊 Statistiques:")
    print(f"   - Personnages avec tags: {with_tags}")
    print(f"   - Personnages sans tags: {without_tags}")
    print(f"   - Total: {with_tags + without_tags}")
    print()
    
    # Afficher quelques exemples
    print("🎯 Exemples de personnages avec tags:")
    cursor.execute("SELECT alias, tags FROM characters WHERE tags != 'AUCUN' ORDER BY alias LIMIT 15")
    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]}")
    
    conn.close()

if __name__ == "__main__":
    check_tags()