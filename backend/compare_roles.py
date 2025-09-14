#!/usr/bin/env python3
"""
Script pour comparer les rôles entre CSV et base de données
"""

import sqlite3
import csv
import os

def compare_roles():
    # Chemins des fichiers
    csv_path = os.path.join("..", "data", "perso.csv")
    db_path = os.path.join("..", "data", "msfdle.db")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 Comparaison détaillée des rôles")
    print("=" * 40)
    
    # Lire tous les rôles du CSV
    csv_roles = {}
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_roles[row['Character Id']] = row['Role']
    
    # Lire tous les rôles de la base
    cursor.execute("SELECT character_id, alias, role FROM characters")
    db_data = cursor.fetchall()
    
    differences = []
    
    for char_id, alias, db_role in db_data:
        if char_id in csv_roles:
            csv_role = csv_roles[char_id]
            if db_role != csv_role:
                differences.append((char_id, alias, db_role, csv_role))
    
    print(f"📊 Différences trouvées: {len(differences)}")
    
    if differences:
        print("\n🔄 Rôles à mettre à jour:")
        for char_id, alias, db_role, csv_role in differences:
            print(f"   📋 {alias} ({char_id}):")
            print(f"      Base: '{db_role}' → CSV: '{csv_role}'")
        
        # Demander confirmation
        print(f"\n❓ Mettre à jour ces {len(differences)} rôles ? (o/n)")
        response = input().lower().strip()
        
        if response == 'o' or response == 'oui':
            print("\n🔄 Mise à jour en cours...")
            for char_id, alias, db_role, csv_role in differences:
                cursor.execute("UPDATE characters SET role = ? WHERE character_id = ?", (csv_role, char_id))
                print(f"   ✅ {alias}: {db_role} → {csv_role}")
            
            conn.commit()
            print(f"\n✅ {len(differences)} rôles mis à jour avec succès!")
        else:
            print("❌ Mise à jour annulée")
    else:
        print("✅ Tous les rôles sont déjà synchronisés!")
    
    conn.close()

if __name__ == "__main__":
    compare_roles()