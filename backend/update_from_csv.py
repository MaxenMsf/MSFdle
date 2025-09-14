#!/usr/bin/env python3
"""
Script pour mettre à jour la base de données avec les modifications du CSV
"""

import sqlite3
import csv
import os

def update_database_from_csv():
    """Met à jour la base de données avec les données du CSV"""
    
    # Chemins des fichiers
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'msfdle.db')
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'perso.csv')
    
    print(f"📂 Base de données: {db_path}")
    print(f"📂 Fichier CSV: {csv_path}")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lire le CSV
    updated_count = 0
    added_count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            character_id = row['Character Id']
            alias = row['Alias']
            alignment = row['Allignement']
            location = row['Localisation']
            origins = row['Origine']
            if row['Origine2']:  # Si il y a une deuxième origine
                origins = f"{origins}, {row['Origine2']}"
            role = row['Role']
            
            # Vérifier si le personnage existe déjà
            cursor.execute("SELECT id, role FROM characters WHERE character_id = ?", (character_id,))
            existing = cursor.fetchone()
            
            if existing:
                existing_id, existing_role = existing
                
                # Mettre à jour le personnage existant (surtout le rôle)
                cursor.execute("""
                    UPDATE characters 
                    SET alias = ?, alignment = ?, location = ?, origins = ?, role = ?
                    WHERE character_id = ?
                """, (alias, alignment, location, origins, role, character_id))
                
                if existing_role != role:
                    print(f"🔄 Mis à jour {alias}: Rôle {existing_role} → {role}")
                    updated_count += 1
                    
            else:
                # Ajouter un nouveau personnage
                cursor.execute("""
                    INSERT INTO characters (character_id, alias, alignment, location, origins, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (character_id, alias, alignment, location, origins, role))
                
                print(f"➕ Ajouté nouveau personnage: {alias} ({role})")
                added_count += 1
    
    # Valider les changements
    conn.commit()
    conn.close()
    
    print(f"\n✅ Mise à jour terminée:")
    print(f"   • {updated_count} personnages mis à jour")
    print(f"   • {added_count} nouveaux personnages ajoutés")

if __name__ == "__main__":
    print("🎯 Mise à jour de la base de données depuis le CSV")
    print("=" * 50)
    update_database_from_csv()