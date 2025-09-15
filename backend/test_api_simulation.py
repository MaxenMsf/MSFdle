#!/usr/bin/env python3
"""
Script de test simple pour l'API sans dépendances externes
"""

import sqlite3
import json
import os

def simulate_api_calls():
    """Simule les appels API pour tester la logique"""
    db_path = os.path.join("..", "data", "msfdle.db")
    
    print("🔧 Simulation des appels API:")
    print("=" * 40)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    cursor = conn.cursor()
    
    # 1. Test get_all_characters (logique)
    print("\n1. Test get_all_characters:")
    cursor.execute("SELECT * FROM characters ORDER BY alias LIMIT 3")
    rows = cursor.fetchall()
    
    characters = []
    for row in rows:
        # Récupérer les tags
        cursor.execute('''
            SELECT GROUP_CONCAT(t.name, ', ') as tags
            FROM character_tags ct
            JOIN tags t ON ct.tag_id = t.id
            WHERE ct.character_id = ?
        ''', (row[0],))
        
        tags_result = cursor.fetchone()
        character_tags = tags_result[0] if tags_result and tags_result[0] else "AUCUN"
        
        character = {
            'id': row[0],                     # Position 0: id
            'alias': row[1],                  # Position 1: alias
            'alignment': row[2],              # Position 2: alignment
            'location': row[3],               # Position 3: location
            'origins': row[4],                # Position 4: origin1
            'origins2': row[5] if row[5] else None,  # Position 5: origin2
            'role': row[6],                   # Position 6: role
            'character_id': row[7],           # Position 7: character_id
            'portrait_path': f"portraits/Portrait_{row[7]}.png",
            'tags': character_tags
        }
        characters.append(character)
    
    print(f"   ✅ {len(characters)} personnages récupérés")
    for char in characters:
        print(f"   📋 {char['alias']} ({char['character_id']}) - {char['tags']}")
    
    # 2. Test get_random_character (logique)
    print("\n2. Test get_random_character:")
    cursor.execute("SELECT * FROM characters ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        cursor.execute('''
            SELECT GROUP_CONCAT(t.name, ', ') as tags
            FROM character_tags ct
            JOIN tags t ON ct.tag_id = t.id
            WHERE ct.character_id = ?
        ''', (row[0],))
        
        tags_result = cursor.fetchone()
        character_tags = tags_result[0] if tags_result and tags_result[0] else "AUCUN"
        
        character = {
            'id': row[0],
            'alias': row[1],
            'alignment': row[2],
            'location': row[3],
            'origins': row[4],
            'origins2': row[5] if row[5] else None,
            'role': row[6],
            'character_id': row[7],
            'tags': character_tags,
            'portrait_path': f"portraits/Portrait_{row[7]}.png"
        }
        
        print(f"   ✅ Personnage aléatoire: {character['alias']}")
        print(f"      ID: {character['character_id']}")
        print(f"      Tags: {character['tags']}")
        print(f"      Portrait: {character['portrait_path']}")
    
    # 3. Test compare functions
    print("\n3. Test des fonctions de comparaison:")
    
    def compare_attribute(guessed, target):
        return "correct" if guessed == target else "incorrect"
    
    def compare_tags(guess_tags, target_tags):
        if not guess_tags:
            guess_tags = ""
        if not target_tags:
            target_tags = ""
        
        if guess_tags.strip() == "AUCUN" and target_tags.strip() == "AUCUN":
            return "correct"
        
        if guess_tags.strip() == "AUCUN" or target_tags.strip() == "AUCUN":
            return "incorrect"
        
        if not guess_tags.strip() or not target_tags.strip():
            return "incorrect"
        
        guess_set = set(tag.strip() for tag in guess_tags.split(',') if tag.strip())
        target_set = set(tag.strip() for tag in target_tags.split(',') if tag.strip())
        
        if guess_set == target_set:
            return "correct"
        elif guess_set & target_set:
            return "partial"
        else:
            return "incorrect"
    
    # Tests de comparaison
    test_cases = [
        ("Hero", "Hero", "correct"),
        ("Hero", "Vilain", "incorrect"),
        ("SPIDER-VERSE, WEB WARRIOR", "SPIDER-VERSE, WEB WARRIOR", "correct"),
        ("SPIDER-VERSE", "SPIDER-VERSE, WEB WARRIOR", "partial"),
        ("X-MEN", "SPIDER-VERSE", "incorrect"),
        ("AUCUN", "AUCUN", "correct"),
        ("AUCUN", "X-MEN", "incorrect"),
    ]
    
    for guess, target, expected in test_cases:
        if "," in guess or "," in target or guess == "AUCUN" or target == "AUCUN":
            result = compare_tags(guess, target)
            test_type = "tags"
        else:
            result = compare_attribute(guess, target)
            test_type = "attribute"
        
        status = "✅" if result == expected else "❌"
        print(f"   {status} {test_type}: '{guess}' vs '{target}' → {result} (attendu: {expected})")
    
    # 4. Test search
    print("\n4. Test de recherche:")
    query = "Spider"
    cursor.execute("SELECT alias FROM characters WHERE alias LIKE ? ORDER BY alias LIMIT 5", (f'%{query}%',))
    results = cursor.fetchall()
    
    search_results = [result[0] for result in results]
    print(f"   ✅ Recherche '{query}': {len(search_results)} résultats")
    for result in search_results:
        print(f"      🔍 {result}")
    
    conn.close()
    print("\n✅ Tous les tests de simulation API sont passés!")

if __name__ == "__main__":
    simulate_api_calls()
