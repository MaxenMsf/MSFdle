#!/usr/bin/env python3
"""
Vérifier les tags des personnages spécifiques des captures d'écran
"""

import sqlite3
import os

def check_specific_tags():
    db_path = os.path.join("..", "data", "msfdle.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Personnages spécifiques à vérifier
    characters_to_check = [
        "GreenGoblinGlider",  # Bouffon vert (classique)
        "UltGreenGoblin",     # Bouffon vert
        "BuckyBarnes",        # Bucky Barnes
        "Bullseye",           # Bullseye
        "Cable",              # Cable
        "Carnage",            # Carnage
        "BlackCat",           # Chatte noire
        "CaptainMarvel",      # Captain Marvel
        "Cosmo",              # Cosmo
        "CorvusGlaive"        # Corvus Glaive
    ]
    
    print("🔍 Vérification des tags des personnages spécifiques:")
    print("=" * 60)
    
    for character_id in characters_to_check:
        # Récupérer les infos du personnage
        cursor.execute("SELECT alias FROM characters WHERE character_id = ?", (character_id,))
        character_result = cursor.fetchone()
        
        if character_result:
            alias = character_result[0]
            
            # Récupérer ses tags
            cursor.execute("""
                SELECT t.name 
                FROM tags t
                JOIN character_tags ct ON t.id = ct.tag_id
                JOIN characters c ON c.id = ct.character_id
                WHERE c.character_id = ?
                ORDER BY t.name
            """, (character_id,))
            
            tags = cursor.fetchall()
            tag_names = [tag[0] for tag in tags]
            
            if tag_names:
                print(f"✅ {alias} ({character_id}): {', '.join(tag_names)}")
            else:
                print(f"❌ {alias} ({character_id}): AUCUN TAG")
        else:
            print(f"⚠️ {character_id}: Personnage non trouvé")
    
    conn.close()

if __name__ == "__main__":
    check_specific_tags()