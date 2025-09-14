#!/usr/bin/env python3
"""
Script pour mettre à jour la base de données avec les modifications du CSV
- Met à jour les rôles des personnages existants
- Ajoute les nouveaux personnages (comme Professeur Xavier)
"""

import sqlite3
import csv
import os

def update_database_from_csv():
    # Chemins des fichiers
    csv_path = os.path.join("..", "data", "perso.csv")
    db_path = os.path.join("..", "data", "msfdle.db")
    
    if not os.path.exists(csv_path):
        print(f"❌ Fichier CSV non trouvé: {csv_path}")
        return
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
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
    cursor.execute("SELECT character_id, alias, alignment, location, origins, role FROM characters")
    existing_characters = cursor.fetchall()
    
    existing_ids = set()
    updates_needed = []
    
    print("🔍 Comparaison avec la base de données...")
    
    for char_data in existing_characters:
        char_id, alias, alignment, location, origins, role = char_data
        existing_ids.add(char_id)
        
        if char_id in characters_from_csv:
            csv_char = characters_from_csv[char_id]
            
            # Vérifier si des mises à jour sont nécessaires
            changes = []
            if csv_char['alias'] != alias:
                changes.append(f"alias: '{alias}' → '{csv_char['alias']}'")
            if csv_char['alignment'] != alignment:
                changes.append(f"alignment: '{alignment}' → '{csv_char['alignment']}'")
            if csv_char['location'] != location:
                changes.append(f"location: '{location}' → '{csv_char['location']}'")
            if csv_char['origins'] != origins:
                changes.append(f"origins: '{origins}' → '{csv_char['origins']}'")
            if csv_char['role'] != role:
                changes.append(f"role: '{role}' → '{csv_char['role']}'")
            
            if changes:
                updates_needed.append((char_id, csv_char, changes))
    
    # Identifier les nouveaux personnages
    new_characters = []
    for char_id, char_data in characters_from_csv.items():
        if char_id not in existing_ids:
            new_characters.append((char_id, char_data))
    
    print(f"📝 {len(updates_needed)} personnages à mettre à jour")
    print(f"➕ {len(new_characters)} nouveaux personnages à ajouter")
    
    # Effectuer les mises à jour
    if updates_needed:
        print("\n🔄 Mise à jour des personnages existants:")
        for char_id, char_data, changes in updates_needed:
            print(f"   📋 {char_id} ({char_data['alias']}):")
            for change in changes:
                print(f"      • {change}")
            
            cursor.execute("""
                UPDATE characters 
                SET alias = ?, alignment = ?, location = ?, origins = ?, role = ?
                WHERE character_id = ?
            """, (char_data['alias'], char_data['alignment'], char_data['location'], 
                  char_data['origins'], char_data['role'], char_id))
    
    # Ajouter les nouveaux personnages
    if new_characters:
        print("\n➕ Ajout des nouveaux personnages:")
        for char_id, char_data in new_characters:
            print(f"   🆕 {char_id} ({char_data['alias']}) - {char_data['role']}")
            
            cursor.execute("""
                INSERT INTO characters (character_id, alias, alignment, location, origins, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (char_id, char_data['alias'], char_data['alignment'], 
                  char_data['location'], char_data['origins'], char_data['role']))
    
    # Valider les changements
    conn.commit()
    conn.close()
    
    print(f"\n✅ Base de données mise à jour avec succès!")
    print(f"   • {len(updates_needed)} personnages mis à jour")
    print(f"   • {len(new_characters)} nouveaux personnages ajoutés")

if __name__ == "__main__":
    print("🎯 Mise à jour de la base de données depuis le CSV")
    print("=" * 50)
    update_database_from_csv()