#!/usr/bin/env python3
"""
Vérification des origines restaurées
"""

import sqlite3
import os

def check_restored_origins():
    db_path = os.path.join("..", "data", "msfdle.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 Vérification des origines restaurées")
    print("=" * 40)
    
    # Vérifier quelques personnages clés
    test_characters = ['Elektra', 'Doom', 'VictoriaHand', 'Ghost', 'Taskmaster']
    
    cursor.execute("SELECT character_id, alias, origins FROM characters WHERE character_id IN ({})".format(
        ','.join('?' * len(test_characters))), test_characters)
    
    results = cursor.fetchall()
    
    for char_id, alias, origins in results:
        print(f"  ✅ {alias} ({char_id}): {origins}")
    
    conn.close()

if __name__ == "__main__":
    check_restored_origins()