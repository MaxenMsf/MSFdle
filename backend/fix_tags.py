#!/usr/bin/env python3
"""
Script pour ajouter les tags manquants puis réappliquer tous les tags
"""

import sqlite3
import os
import sys

# Ajouter le répertoire parent pour importer character_tags
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from character_tags import character_tags

def add_missing_tags_and_reapply():
    db_path = os.path.join("..", "data", "msfdle.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🏷️ Ajout des tags manquants et réapplication...")
    
    # Collecter tous les tags uniques depuis character_tags
    all_tags = set()
    for character_id, tags in character_tags.items():
        for tag in tags:
            if tag != "AUCUN":
                all_tags.add(tag)
    
    print(f"📊 {len(all_tags)} tags uniques trouvés")
    
    # Ajouter tous les tags manquants
    tags_added = 0
    for tag_name in all_tags:
        cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
        if cursor.rowcount > 0:
            tags_added += 1
            print(f"   ➕ Ajouté: {tag_name}")
    
    print(f"✅ {tags_added} nouveaux tags ajoutés")
    
    # Supprimer toutes les associations existantes pour recommencer
    cursor.execute("DELETE FROM character_tags")
    print("🗑️ Anciennes associations supprimées")
    
    # Réappliquer tous les tags
    associations_created = 0
    characters_with_tags = 0
    
    for character_id, tags in character_tags.items():
        # Vérifier si le personnage existe
        cursor.execute("SELECT id FROM characters WHERE character_id = ?", (character_id,))
        character_result = cursor.fetchone()
        
        if character_result:
            character_db_id = character_result[0]
            character_has_tags = False
            
            for tag_name in tags:
                if tag_name != "AUCUN":
                    # Récupérer l'ID du tag
                    cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
                    tag_result = cursor.fetchone()
                    
                    if tag_result:
                        tag_id = tag_result[0]
                        
                        # Créer l'association
                        cursor.execute("""
                            INSERT OR IGNORE INTO character_tags (character_id, tag_id) 
                            VALUES (?, ?)
                        """, (character_db_id, tag_id))
                        
                        if cursor.rowcount > 0:
                            associations_created += 1
                            character_has_tags = True
            
            if character_has_tags:
                characters_with_tags += 1
        else:
            print(f"⚠️ Personnage '{character_id}' non trouvé dans la base")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Réapplication terminée!")
    print(f"   • {associations_created} associations créées")
    print(f"   • {characters_with_tags} personnages avec tags")
    
    return True

if __name__ == "__main__":
    add_missing_tags_and_reapply()