#!/usr/bin/env python3
"""
Script pour reconstruire complètement la base de données depuis le CSV
- Lit le nouveau format CSV avec les tags intégrés
- Recrée la base de données avec la nouvelle structure
- Parse les tags séparés par des virgules dans la colonne Tags
"""

import sqlite3
import csv
import os
import re

def parse_tags(tags_string):
    """Parse la chaîne de tags et retourne une liste de tags uniques"""
    if not tags_string or tags_string.strip() == '':
        return []
    
    # Enlever les guillemets extérieurs si présents
    tags_string = tags_string.strip('"')
    
    # Séparer par les virgules et nettoyer
    tags = []
    for tag in tags_string.split(','):
        tag = tag.strip()
        if tag:
            tags.append(tag)
    
    return tags

def rebuild_database_from_csv():
    # Chemins des fichiers
    csv_path = os.path.join("..", "data", "perso.csv")
    db_path = os.path.join("..", "data", "msfdle.db")
    
    if not os.path.exists(csv_path):
        print(f"❌ Fichier CSV non trouvé: {csv_path}")
        return
    
    # Supprimer l'ancienne base si elle existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Ancienne base de données supprimée")
    
    # Créer la nouvelle base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🏗️ Création de la nouvelle structure de base de données...")
    
    # Lire et exécuter le schéma
    schema_path = os.path.join("..", "database", "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as schema_file:
            schema_sql = schema_file.read()
            cursor.executescript(schema_sql)
    else:
        # Créer la structure de base si le fichier schema n'existe pas
        cursor.executescript("""
            CREATE TABLE characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias VARCHAR(200) UNIQUE NOT NULL,
                alignment VARCHAR(20) NOT NULL,
                location VARCHAR(50) NOT NULL,
                origin1 VARCHAR(50) NOT NULL,
                origin2 VARCHAR(50),
                role VARCHAR(50) NOT NULL,
                character_id VARCHAR(100) UNIQUE NOT NULL
            );

            CREATE TABLE tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE NOT NULL
            );

            CREATE TABLE character_tags (
                character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
                tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
                PRIMARY KEY (character_id, tag_id)
            );

            CREATE INDEX idx_characters_alignment ON characters(alignment);
            CREATE INDEX idx_characters_location ON characters(location);
            CREATE INDEX idx_characters_origin1 ON characters(origin1);
            CREATE INDEX idx_characters_origin2 ON characters(origin2);
            CREATE INDEX idx_characters_role ON characters(role);
            CREATE INDEX idx_characters_character_id ON characters(character_id);
            CREATE INDEX idx_character_tags_character ON character_tags(character_id);
        """)
    
    print("📖 Lecture du fichier CSV...")
    
    # Lire le CSV et collecter tous les tags
    characters_data = []
    all_tags = set()
    
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Parse les origines
            origin1 = row['Origine'] if row['Origine'] else None
            origin2 = row['Origine2'] if row['Origine2'] else None
            
            # Parse les tags
            tags = parse_tags(row['Tags'])
            all_tags.update(tags)
            
            character_data = {
                'character_id': row['Character Id'],
                'alias': row['Alias'],
                'alignment': row['Allignement'],
                'location': row['Localisation'],
                'origin1': origin1,
                'origin2': origin2,
                'role': row['Role'],
                'tags': tags
            }
            characters_data.append(character_data)
    
    print(f"📊 {len(characters_data)} personnages trouvés dans le CSV")
    print(f"🏷️ {len(all_tags)} tags uniques trouvés")
    
    # Insérer tous les tags
    print("🏷️ Insertion des tags...")
    tag_ids = {}
    for tag in sorted(all_tags):
        cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag,))
        tag_ids[tag] = cursor.lastrowid
    
    # Insérer tous les personnages
    print("👥 Insertion des personnages...")
    character_ids = {}
    for char_data in characters_data:
        cursor.execute("""
            INSERT INTO characters (alias, alignment, location, origin1, origin2, role, character_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (char_data['alias'], char_data['alignment'], char_data['location'],
              char_data['origin1'], char_data['origin2'], char_data['role'], char_data['character_id']))
        
        character_ids[char_data['character_id']] = cursor.lastrowid
    
    # Associer les tags aux personnages
    print("🔗 Association des tags aux personnages...")
    for char_data in characters_data:
        character_db_id = character_ids[char_data['character_id']]
        for tag in char_data['tags']:
            tag_id = tag_ids[tag]
            cursor.execute("""
                INSERT INTO character_tags (character_id, tag_id)
                VALUES (?, ?)
            """, (character_db_id, tag_id))
    
    # Valider les changements
    conn.commit()
    
    # Afficher quelques statistiques
    cursor.execute("SELECT COUNT(*) FROM characters")
    char_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tags")
    tag_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM character_tags")
    relation_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ Base de données reconstruite avec succès!")
    print(f"   • {char_count} personnages")
    print(f"   • {tag_count} tags")
    print(f"   • {relation_count} associations personnage-tag")

def test_database():
    """Test rapide pour vérifier que la base fonctionne"""
    db_path = os.path.join("..", "data", "msfdle.db")
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée pour le test")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n🧪 Test de la base de données:")
    
    # Test: récupérer un personnage avec ses tags
    cursor.execute("""
        SELECT c.alias, c.alignment, c.location, c.origin1, c.origin2, c.role, c.character_id,
               GROUP_CONCAT(t.name, ', ') as tags
        FROM characters c
        LEFT JOIN character_tags ct ON c.id = ct.character_id
        LEFT JOIN tags t ON ct.tag_id = t.id
        WHERE c.alias LIKE '%Cyclope%' OR c.alias LIKE '%Spider%'
        GROUP BY c.id
        LIMIT 3
    """)
    
    results = cursor.fetchall()
    for result in results:
        alias, alignment, location, origin1, origin2, role, character_id, tags = result
        print(f"   📋 {alias} ({character_id}):")
        print(f"      Alignement: {alignment}, Localisation: {location}")
        print(f"      Origines: {origin1}" + (f", {origin2}" if origin2 else ""))
        print(f"      Rôle: {role}")
        print(f"      Tags: {tags if tags else 'Aucun'}")
        print(f"      Portrait: Portrait_{character_id}.png")
        print()
    
    conn.close()

if __name__ == "__main__":
    print("🎯 Reconstruction complète de la base de données depuis le CSV")
    print("=" * 60)
    rebuild_database_from_csv()
    test_database()
