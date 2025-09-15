#!/usr/bin/env python3
"""
Script de test pour vérifier la nouvelle structure de base de données
"""

import sqlite3
import os

def test_database():
    """Test complet de la base de données"""
    db_path = os.path.join("..", "data", "msfdle.db")
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🧪 Tests de la base de données:")
    print("=" * 50)
    
    # Test 1: Structure des tables
    print("\n1. Vérification de la structure:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"   Tables: {', '.join(tables)}")
    
    # Test 2: Comptage des données
    print("\n2. Comptage des données:")
    cursor.execute("SELECT COUNT(*) FROM characters")
    char_count = cursor.fetchone()[0]
    print(f"   Personnages: {char_count}")
    
    cursor.execute("SELECT COUNT(*) FROM tags")
    tag_count = cursor.fetchone()[0]
    print(f"   Tags: {tag_count}")
    
    cursor.execute("SELECT COUNT(*) FROM character_tags")
    relation_count = cursor.fetchone()[0]
    print(f"   Relations personnage-tag: {relation_count}")
    
    # Test 3: Quelques personnages avec leurs tags
    print("\n3. Exemples de personnages avec tags:")
    cursor.execute("""
        SELECT c.alias, c.character_id, c.alignment, c.location, c.role,
               GROUP_CONCAT(t.name, ', ') as tags
        FROM characters c
        LEFT JOIN character_tags ct ON c.id = ct.character_id
        LEFT JOIN tags t ON ct.tag_id = t.id
        WHERE c.alias LIKE '%Spider%' OR c.alias LIKE '%Captain%' OR c.alias LIKE '%Cyclope%'
        GROUP BY c.id
        LIMIT 5
    """)
    
    results = cursor.fetchall()
    for result in results:
        alias, character_id, alignment, location, role, tags = result
        print(f"   📋 {alias} ({character_id}):")
        print(f"      {alignment} - {location} - {role}")
        print(f"      Tags: {tags if tags else 'Aucun'}")
        print(f"      Portrait: Portrait_{character_id}.png")
        print()
    
    # Test 4: Tags les plus populaires
    print("4. Tags les plus populaires:")
    cursor.execute("""
        SELECT t.name, COUNT(ct.character_id) as count
        FROM tags t
        LEFT JOIN character_tags ct ON t.id = ct.tag_id
        GROUP BY t.id, t.name
        ORDER BY count DESC
        LIMIT 10
    """)
    
    popular_tags = cursor.fetchall()
    for tag_name, count in popular_tags:
        print(f"   🏷️ {tag_name}: {count} personnages")
    
    # Test 5: Vérification de la correspondance des portraits
    print("\n5. Vérification des portraits:")
    portraits_path = os.path.join("..", "frontend", "portraits")
    if os.path.exists(portraits_path):
        portraits = [f for f in os.listdir(portraits_path) if f.startswith("Portrait_") and f.endswith(".png")]
        portrait_ids = [f.replace("Portrait_", "").replace(".png", "") for f in portraits]
        
        cursor.execute("SELECT character_id FROM characters WHERE character_id IN ({})".format(','.join(['?' for _ in portrait_ids])), portrait_ids)
        found_chars = [row[0] for row in cursor.fetchall()]
        
        print(f"   Portraits disponibles: {len(portraits)}")
        print(f"   Personnages avec portraits: {len(found_chars)}")
        
        # Quelques exemples de correspondance
        cursor.execute("SELECT alias, character_id FROM characters WHERE character_id IN ({}) LIMIT 5".format(','.join(['?' for _ in portrait_ids[:5]])), portrait_ids[:5])
        examples = cursor.fetchall()
        for alias, char_id in examples:
            print(f"   ✅ {alias} → Portrait_{char_id}.png")
    else:
        print("   ⚠️ Dossier portraits non trouvé")
    
    conn.close()
    print("\n✅ Tests terminés!")

def test_specific_functions():
    """Test des fonctions spécifiques"""
    db_path = os.path.join("..", "data", "msfdle.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n🔧 Test des fonctions spécifiques:")
    print("=" * 50)
    
    # Test: récupérer un personnage aléatoire
    print("\n1. Personnage aléatoire:")
    cursor.execute("SELECT * FROM characters ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        # Récupérer les tags
        cursor.execute('''
            SELECT GROUP_CONCAT(t.name, ', ') as tags
            FROM character_tags ct
            JOIN tags t ON ct.tag_id = t.id
            WHERE ct.character_id = ?
        ''', (row[0],))
        
        tags_result = cursor.fetchone()
        character_tags = tags_result[0] if tags_result and tags_result[0] else "AUCUN"
        
        print(f"   📋 {row[1]} ({row[7]}):")  # alias, character_id
        print(f"      Alignement: {row[2]}, Localisation: {row[3]}")
        print(f"      Origines: {row[4]}" + (f", {row[5]}" if row[5] else ""))
        print(f"      Rôle: {row[6]}")
        print(f"      Tags: {character_tags}")
        print(f"      Portrait: Portrait_{row[7]}.png")
    
    # Test: recherche de personnages
    print("\n2. Recherche 'Spider':")
    cursor.execute("SELECT alias FROM characters WHERE alias LIKE ? ORDER BY alias LIMIT 5", ('%Spider%',))
    spiders = cursor.fetchall()
    for spider in spiders:
        print(f"   🕷️ {spider[0]}")
    
    conn.close()

if __name__ == "__main__":
    test_database()
    test_specific_functions()
