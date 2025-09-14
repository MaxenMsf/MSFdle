#!/usr/bin/env python3
"""
Script pour trouver les vrais IDs des personnages des captures d'écran
"""

import sqlite3
import os

def find_character_ids():
    db_path = os.path.join("..", "data", "msfdle.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Liste des personnages des captures d'écran
    search_terms = [
        "Bouffon", "Green", "Goblin", "Brawn", "Bucky", "Bullseye", "Cable", 
        "Cape", "Captain", "Carnage", "Chatte", "Noir", "Chercheuse", "Chevalier", 
        "Circe", "Cogneur", "Colleen", "Colosse", "Colossus", "Corvus", "Cosmic", 
        "Cosmo", "Crâne", "Rouge"
    ]
    
    print("🔍 Recherche des personnages des captures d'écran:")
    
    for term in search_terms:
        cursor.execute("SELECT character_id, alias FROM characters WHERE alias LIKE ?", (f"%{term}%",))
        results = cursor.fetchall()
        
        if results:
            print(f"\n📋 Terme '{term}':")
            for char_id, alias in results:
                print(f"   {char_id} - {alias}")
    
    conn.close()

if __name__ == "__main__":
    find_character_ids()