#!/usr/bin/env python3
"""
Vérification du contenu des tables de tags
"""
import sqlite3

def check_tags_content():
    conn = sqlite3.connect('../data/msfdle.db')
    cursor = conn.cursor()
    
    print("🏷️ Contenu des tables de tags")
    print("=" * 50)
    
    # Compter les tags disponibles
    cursor.execute("SELECT COUNT(*) FROM tags")
    tag_count = cursor.fetchone()[0]
    print(f"📊 Nombre de tags disponibles: {tag_count}")
    
    # Lister quelques tags
    print("\n🏷️ Exemples de tags disponibles:")
    cursor.execute("SELECT name FROM tags ORDER BY name LIMIT 15")
    for row in cursor.fetchall():
        print(f"   - {row[0]}")
    
    # Compter les associations personnage-tags
    cursor.execute("SELECT COUNT(*) FROM character_tags")
    assoc_count = cursor.fetchone()[0]
    print(f"\n🔗 Nombre d'associations personnage-tags: {assoc_count}")
    
    # Personnages avec tags
    print("\n🎯 Personnages avec leurs tags:")
    cursor.execute("""
        SELECT c.alias, GROUP_CONCAT(t.name, ', ') as tags
        FROM characters c
        JOIN character_tags ct ON c.id = ct.character_id
        JOIN tags t ON ct.tag_id = t.id
        GROUP BY c.id, c.alias
        ORDER BY c.alias
        LIMIT 15
    """)
    
    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]}")
    
    # Compter personnages avec tags
    cursor.execute("""
        SELECT COUNT(DISTINCT character_id) FROM character_tags
    """)
    chars_with_tags = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM characters")
    total_chars = cursor.fetchone()[0]
    
    chars_without_tags = total_chars - chars_with_tags
    
    print(f"\n📊 Statistiques:")
    print(f"   - Personnages avec tags: {chars_with_tags}")
    print(f"   - Personnages sans tags: {chars_without_tags}")
    print(f"   - Total personnages: {total_chars}")
    
    conn.close()

if __name__ == "__main__":
    check_tags_content()