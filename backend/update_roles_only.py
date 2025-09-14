#!/usr/bin/env python3
"""
Script pour mettre à jour UNIQUEMENT les rôles et ajouter les nouveaux personnages
"""

import sqlite3
import csv
import os

def update_roles_and_new_characters():
    # Chemins des fichiers
    csv_path = os.path.join("..", "data", "perso.csv")
    db_path = os.path.join("..", "data", "msfdle.db")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📖 Lecture du fichier CSV...")
    
    # Lire le CSV
    characters_from_csv = {}
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            character_id = row['Character Id']
            characters_from_csv[character_id] = {
                'alias': row['Alias'],
                'alignment': row['Allignement'],
                'location': row['Localisation'],
                'origins': row['Origine'],
                'role': row['Role']
            }
    
    print(f"📊 {len(characters_from_csv)} personnages trouvés dans le CSV")
    
    # Récupérer les personnages existants dans la base
    cursor.execute("SELECT character_id, alias, role FROM characters")
    existing_characters = cursor.fetchall()
    
    existing_ids = set()
    role_updates = []
    
    print("🔍 Vérification des rôles...")
    
    for char_data in existing_characters:
        char_id, alias, current_role = char_data
        existing_ids.add(char_id)
        
        if char_id in characters_from_csv:
            csv_char = characters_from_csv[char_id]
            
            # Vérifier si le rôle a changé
            if csv_char['role'] != current_role:
                role_updates.append((char_id, alias, current_role, csv_char['role']))
    
    # Identifier les nouveaux personnages
    new_characters = []
    for char_id, char_data in characters_from_csv.items():
        if char_id not in existing_ids:
            new_characters.append((char_id, char_data))
    
    print(f"📝 {len(role_updates)} rôles à mettre à jour")
    print(f"➕ {len(new_characters)} nouveaux personnages à ajouter")
    
    # Effectuer les mises à jour de rôles
    if role_updates:
        print("\n🔄 Mise à jour des rôles:")
        for char_id, alias, old_role, new_role in role_updates:
            print(f"   📋 {alias} ({char_id}): '{old_role}' → '{new_role}'")
            
            cursor.execute("""
                UPDATE characters 
                SET role = ?
                WHERE character_id = ?
            """, (new_role, char_id))
    
    # Ajouter les nouveaux personnages
    if new_characters:
        print("\n➕ Ajout des nouveaux personnages:")
        for char_id, char_data in new_characters:
            print(f"   🆕 {char_data['alias']} ({char_id}) - Rôle: {char_data['role']}")
            
            cursor.execute("""
                INSERT INTO characters (character_id, alias, alignment, location, origins, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (char_id, char_data['alias'], char_data['alignment'], 
                  char_data['location'], char_data['origins'], char_data['role']))
    
    # Valider les changements
    conn.commit()
    conn.close()
    
    print(f"\n✅ Mise à jour terminée!")
    print(f"   • {len(role_updates)} rôles mis à jour")
    print(f"   • {len(new_characters)} nouveaux personnages ajoutés")

if __name__ == "__main__":
    print("🎯 Mise à jour des rôles et ajout de nouveaux personnages")
    print("=" * 55)
    update_roles_and_new_characters()