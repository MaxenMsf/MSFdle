#!/usr/bin/env python3
import sqlite3
import os

# Configuration de la base de données SQLite
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'msfdle.db')

def check_characters():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Vérifier Adam Warlock
    cursor.execute("SELECT * FROM characters WHERE alias = 'Adam Warlock'")
    adam = cursor.fetchone()
    print("Adam Warlock:", adam)
    
    # Vérifier Docteur Fatalis
    cursor.execute("SELECT * FROM characters WHERE alias = 'Docteur fatalis'")
    fatalis = cursor.fetchone()
    print("Docteur fatalis:", fatalis)
    
    # Vérifier les tags
    if adam:
        cursor.execute('''
            SELECT GROUP_CONCAT(t.name, ', ') as tags
            FROM character_tags ct
            JOIN tags t ON ct.tag_id = t.id
            WHERE ct.character_id = ?
        ''', (adam[0],))
        adam_tags = cursor.fetchone()
        print("Tags Adam Warlock:", adam_tags[0] if adam_tags and adam_tags[0] else "AUCUN")
    
    if fatalis:
        cursor.execute('''
            SELECT GROUP_CONCAT(t.name, ', ') as tags
            FROM character_tags ct
            JOIN tags t ON ct.tag_id = t.id
            WHERE ct.character_id = ?
        ''', (fatalis[0],))
        fatalis_tags = cursor.fetchone()
        print("Tags Docteur fatalis:", fatalis_tags[0] if fatalis_tags and fatalis_tags[0] else "AUCUN")
    
    conn.close()

if __name__ == "__main__":
    check_characters()