#!/usr/bin/env python3
"""
Script pour appliquer les tags aux personnages dans la base de données MSFdle
"""

import sqlite3
import os
import sys

# Ajouter le répertoire data au path pour importer character_tags
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

try:
    from character_tags import character_tags, available_tags
except ImportError:
    print("❌ Erreur: Impossible d'importer character_tags.py")
    print("📁 Assurez-vous que le fichier data/character_tags.py existe")
    sys.exit(1)

# Configuration de la base de données SQLite
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'msfdle.db')

def apply_tags_to_database():
    """Applique les tags aux personnages dans la base de données"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # 1. D'abord, ajouter tous les tags disponibles dans la table tags
        print("🏷️ Ajout des tags disponibles...")
        tags_added = 0
        for tag_name in available_tags:
            try:
                cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
                if cursor.rowcount > 0:
                    tags_added += 1
            except Exception as e:
                print(f"⚠️ Erreur lors de l'ajout du tag '{tag_name}': {e}")
        
        print(f"✅ {tags_added} nouveaux tags ajoutés")
        
        # 2. Ensuite, associer les tags aux personnages
        print("🔗 Association des tags aux personnages...")
        associations_added = 0
        characters_updated = 0
        
        for character_id, tags_list in character_tags.items():
            # Récupérer l'ID du personnage
            cursor.execute("SELECT id FROM characters WHERE character_id = ?", (character_id,))
            char_result = cursor.fetchone()
            
            if not char_result:
                print(f"⚠️ Personnage '{character_id}' non trouvé dans la base")
                continue
            
            char_db_id = char_result[0]
            characters_updated += 1
            
            # Supprimer les anciennes associations pour ce personnage
            cursor.execute("DELETE FROM character_tags WHERE character_id = ?", (char_db_id,))
            
            # Ajouter les nouveaux tags
            for tag_name in tags_list:
                # Récupérer l'ID du tag
                cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
                tag_result = cursor.fetchone()
                
                if tag_result:
                    tag_id = tag_result[0]
                    cursor.execute("INSERT INTO character_tags (character_id, tag_id) VALUES (?, ?)", 
                                 (char_db_id, tag_id))
                    associations_added += 1
                else:
                    print(f"⚠️ Tag '{tag_name}' non trouvé pour '{character_id}'")
        
        conn.commit()
        
        # 3. Vérification des résultats
        cursor.execute("SELECT COUNT(*) FROM tags")
        total_tags = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM character_tags")
        total_associations = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(DISTINCT ct.character_id) 
            FROM character_tags ct
        """)
        characters_with_tags = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM characters")
        total_characters = cursor.fetchone()[0]
        
        characters_without_tags = total_characters - characters_with_tags
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Tags appliqués avec succès!")
        print(f"📊 Résumé:")
        print(f"   - Tags disponibles: {total_tags}")
        print(f"   - Associations créées: {associations_added}")
        print(f"   - Personnages avec tags: {characters_with_tags}")
        print(f"   - Personnages sans tags: {characters_without_tags} (afficheront 'AUCUN')")
        print(f"   - Total personnages: {total_characters}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'application des tags: {e}")
        return False

def show_characters_with_tags():
    """Affiche quelques exemples de personnages avec leurs tags"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.alias, c.character_id, GROUP_CONCAT(t.name, ', ') as tags
            FROM characters c
            LEFT JOIN character_tags ct ON c.id = ct.character_id
            LEFT JOIN tags t ON ct.tag_id = t.id
            GROUP BY c.id, c.alias, c.character_id
            ORDER BY c.alias
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        
        print(f"\n🎯 Exemples de personnages avec tags:")
        for alias, character_id, tags in results:
            tags_display = tags if tags else "AUCUN"
            print(f"   - {alias} ({character_id}): {tags_display}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage: {e}")

if __name__ == "__main__":
    print("🎮 Application des tags MSFdle")
    print("=" * 50)
    
    # Vérifier que la base existe
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Base de données non trouvée: {DATABASE_PATH}")
        print("📋 Exécutez d'abord update_db_with_character_id.py")
        sys.exit(1)
    
    # Appliquer les tags
    if apply_tags_to_database():
        show_characters_with_tags()
        print(f"\n🎉 Tags appliqués! Les personnages sans tags afficheront 'AUCUN'")
    else:
        print(f"\n❌ Échec de l'application des tags")
        sys.exit(1)