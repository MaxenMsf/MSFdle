#!/usr/bin/env python3
"""
Script pour restaurer les origines multiples des personnages
"""

import sqlite3
import os

def restore_multiple_origins():
    db_path = os.path.join("..", "data", "msfdle.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔄 Restauration des origines multiples...")
    
    # Liste des personnages avec leurs origines correctes (2 origines)
    characters_with_multiple_origins = [
        ('Elektra', 'Mystique, Expertise'),
        ('Ghost', 'Techno, Biotechnique'), 
        ('Taskmaster', 'Expertise, Biotechnique'),
        ('Sybil', 'Expertise, Techno'),
        ('GhostSpider', 'Biotechnique, Expertise'),
        ('Doom', 'Mystique, Techno'),
        ('SpiderManNoir', 'Mystique, Expertise'),
        ('PeterBParker', 'Biotechnique, Expertise'),
        ('SpiderManPavitr', 'Biotechnique, Expertise'),
        ('PeniParker', 'Expertise, Techno'),
        ('ZombieScarletWitch', 'Biotechnique, Mystique'),
        ('VictoriaHand', 'Biotechnique, Techno')
    ]
    
    print(f"📋 Personnages à restaurer: {len(characters_with_multiple_origins)}")
    
    for character_id, correct_origins in characters_with_multiple_origins:
        # Vérifier l'origine actuelle
        cursor.execute("SELECT alias, origins FROM characters WHERE character_id = ?", (character_id,))
        result = cursor.fetchone()
        
        if result:
            alias, current_origins = result
            print(f"   🔄 {alias} ({character_id}):")
            print(f"      Actuel: '{current_origins}' → Correct: '{correct_origins}'")
            
            # Mettre à jour
            cursor.execute("UPDATE characters SET origins = ? WHERE character_id = ?", 
                         (correct_origins, character_id))
        else:
            print(f"   ❌ {character_id} non trouvé dans la base")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Origines restaurées avec succès!")

if __name__ == "__main__":
    print("🎯 Restauration des origines multiples")
    print("=" * 40)
    restore_multiple_origins()