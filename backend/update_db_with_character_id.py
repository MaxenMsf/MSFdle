import sqlite3
import csv
import os

# Configuration de la base de données SQLite
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'msfdle.db')

def update_database_with_character_id():
    """Met à jour la base de données pour inclure le character_id"""
    try:
        # Supprimer l'ancienne base
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
            print("✅ Ancienne base supprimée")
        
        # Créer la nouvelle base avec character_id
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Créer la table characters avec character_id
        cursor.execute('''
            CREATE TABLE characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id TEXT NOT NULL UNIQUE,
                alias TEXT NOT NULL,
                alignment TEXT NOT NULL,
                location TEXT NOT NULL,
                origins TEXT NOT NULL,
                role TEXT NOT NULL,
                origins2 TEXT,
                tags TEXT DEFAULT ""
            )
        ''')
        
        # Créer les tables pour les tags
        cursor.execute('''
            CREATE TABLE tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE character_tags (
                character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
                tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
                PRIMARY KEY (character_id, tag_id)
            )
        ''')
        
        # Importer les données du CSV avec character_id
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'perso.csv')
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                origin1 = row["Origine"].strip()
                origin2 = row["Origine2"].strip() if row["Origine2"].strip() else ""
                
                combined_origins = f"{origin1}, {origin2}" if origin2 else origin1
                
                cursor.execute('''
                    INSERT INTO characters (character_id, alias, alignment, location, origins, role, origins2)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row["Character Id"].strip(),
                    row["Alias"].strip(),
                    row["Allignement"].strip(),
                    row["Localisation"].strip(),
                    combined_origins,
                    row["Role"].strip(),
                    origin2 if origin2 else None
                ))
        
        conn.commit()
        
        # Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT character_id, alias FROM characters LIMIT 5")
        samples = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print(f"✅ Base mise à jour avec {count} personnages")
        print("📋 Exemples de character_id:")
        for char_id, alias in samples:
            print(f"  - {alias}: {char_id}")
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

if __name__ == "__main__":
    update_database_with_character_id()