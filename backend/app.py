from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"], allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"])

# Configuration de la base de données SQLite
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'msfdle.db')

def get_db_connection():
    """Crée une connexion à la base de données SQLite"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        print(f"🔗 Connexion à la base: {DATABASE_PATH}")
        return connection
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

@app.route('/')
def serve_game():
    """Sert le jeu MSFdle"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'test_game_clean.html')
    try:
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Jeu non trouvé", 404

@app.route('/admin')
def admin():
    """Sert l'interface d'administration des tags"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'admin_tags.html')
    try:
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Interface d'admin non trouvée", 404

@app.route('/portraits/<filename>')
def serve_portrait(filename):
    """Sert les portraits des personnages"""
    portraits_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'portraits')
    try:
        return send_from_directory(portraits_path, filename)
    except FileNotFoundError:
        # Retourner un portrait par défaut ou une erreur 404
        return jsonify({"error": "Portrait non trouvé"}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état de l'API"""
    return jsonify({"status": "healthy", "message": "MSFdle API is running!"})

@app.route('/api/test-db', methods=['GET'])
def test_database():
    """Test de la base de données"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Impossible de se connecter à la base"}), 500
        
        cursor = conn.cursor()
        
        # Test tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Test données
        cursor.execute("SELECT COUNT(*) FROM characters")
        char_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tags")
        tag_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "tables": tables,
            "characters": char_count,
            "tags": tag_count,
            "message": "Base de données accessible"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fix-database', methods=['GET'])
def fix_database():
    """Corrige la base de données"""
    try:
        import csv
        
        # Supprimer l'ancienne base
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
            print("✅ Ancienne base supprimée")
        
        # Créer la nouvelle base
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Créer la table avec la bonne structure
        cursor.execute('''
            CREATE TABLE characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias TEXT NOT NULL,
                alignment TEXT NOT NULL,
                location TEXT NOT NULL,
                origins TEXT NOT NULL,
                role TEXT NOT NULL
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
        
        # Importer les données du CSV
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'perso.csv')
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                origin1 = row["Origine"].strip()
                origin2 = row["Origine2"].strip() if row["Origine2"].strip() else ""
                
                combined_origins = f"{origin1}, {origin2}" if origin2 else origin1
                
                cursor.execute('''
                    INSERT INTO characters (alias, alignment, location, origins, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    row["Alias"].strip(),
                    row["Allignement"].strip(),
                    row["Localisation"].strip(),
                    combined_origins,
                    row["Role"].strip()
                ))
        
        conn.commit()
        
        # Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({"status": "success", "message": f"Base corrigée avec {count} personnages"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/replace-support', methods=['GET'])
def replace_support_with_soutien():
    """Remplace tous les 'Support' par 'Soutien' dans le CSV et recrée la base"""
    try:
        import csv
        
        # 1. Modifier le CSV
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'perso.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        support_count = content.count(',Support')
        content = content.replace(',Support', ',Soutien')
        
        with open(csv_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        # 2. Recréer la base de données
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Créer les tables
        cursor.execute('''
            CREATE TABLE characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias TEXT NOT NULL,
                alignment TEXT NOT NULL,
                location TEXT NOT NULL,
                origins TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
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
        
        # Importer les données du CSV modifié
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                origin1 = row["Origine"].strip()
                origin2 = row["Origine2"].strip() if row["Origine2"].strip() else ""
                
                combined_origins = f"{origin1}, {origin2}" if origin2 else origin1
                
                cursor.execute('''
                    INSERT INTO characters (alias, alignment, location, origins, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    row["Alias"].strip(),
                    row["Allignement"].strip(),
                    row["Localisation"].strip(),
                    combined_origins,
                    row["Role"].strip()
                ))
        
        conn.commit()
        
        # Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM characters WHERE role = 'Soutien'")
        soutien_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "success", 
            "message": f"CSV et base mis à jour: {support_count} 'Support' remplacés par 'Soutien'. {count} personnages importés, dont {soutien_count} en rôle Soutien."
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/tags', methods=['GET'])
def get_all_tags():
    """Récupère tous les tags"""
    try:
        print("🏷️ Récupération des tags...")
        conn = get_db_connection()
        if not conn:
            print("❌ Erreur de connexion à la base")
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tags ORDER BY name")
        rows = cursor.fetchall()
        
        print(f"📊 {len(rows)} tags trouvés")
        
        tags = []
        for row in rows:
            tags.append({
                'id': row[0],
                'name': row[1]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(tags)
    
    except Exception as e:
        print(f"❌ Erreur get_all_tags: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tags', methods=['POST'])
def create_tag():
    """Crée un nouveau tag"""
    try:
        data = request.get_json()
        tag_name = data.get('name', '').strip()
        
        if not tag_name:
            return jsonify({"error": "Le nom du tag est requis"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
        tag_id = cursor.lastrowid
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"id": tag_id, "name": tag_name}), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "Ce tag existe déjà"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<int:character_id>/tags', methods=['GET'])
def get_character_tags(character_id):
    """Récupère les tags d'un personnage"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.name 
            FROM tags t
            JOIN character_tags ct ON t.id = ct.tag_id
            WHERE ct.character_id = ?
            ORDER BY t.name
        """, (character_id,))
        rows = cursor.fetchall()
        
        tags = []
        for row in rows:
            tags.append({
                'id': row[0],
                'name': row[1]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(tags)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<int:character_id>/tags/<int:tag_id>', methods=['POST'])
def add_tag_to_character(character_id, tag_id):
    """Ajoute un tag à un personnage"""
    try:
        print(f"🏷️ Ajout du tag {tag_id} au personnage {character_id}")
        conn = get_db_connection()
        if not conn:
            print("❌ Erreur de connexion à la base")
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # Vérifier que le personnage existe
        cursor.execute("SELECT id FROM characters WHERE id = ?", (character_id,))
        if not cursor.fetchone():
            print(f"❌ Personnage {character_id} non trouvé")
            return jsonify({"error": "Personnage non trouvé"}), 404
        
        # Vérifier que le tag existe
        cursor.execute("SELECT id FROM tags WHERE id = ?", (tag_id,))
        if not cursor.fetchone():
            print(f"❌ Tag {tag_id} non trouvé")
            return jsonify({"error": "Tag non trouvé"}), 404
        
        cursor.execute("INSERT INTO character_tags (character_id, tag_id) VALUES (?, ?)", 
                      (character_id, tag_id))
        conn.commit()
        
        print(f"✅ Tag {tag_id} ajouté au personnage {character_id}")
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Tag ajouté au personnage"}), 201
    
    except sqlite3.IntegrityError as e:
        print(f"⚠️ Contrainte d'intégrité: {e}")
        return jsonify({"error": "Ce tag est déjà associé à ce personnage"}), 409
    except Exception as e:
        print(f"❌ Erreur add_tag_to_character: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<int:character_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_character(character_id, tag_id):
    """Supprime un tag d'un personnage"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM character_tags WHERE character_id = ? AND tag_id = ?", 
                      (character_id, tag_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Tag supprimé du personnage"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters', methods=['GET'])
def get_all_characters():
    """Récupère tous les personnages"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM characters ORDER BY alias")
        rows = cursor.fetchall()
        
        print(f"📊 Trouvé {len(rows)} personnages dans la base")
        if rows:
            print(f"🎯 Premier personnage: {dict(rows[0])}")
        
        # Convertir les résultats en dictionnaires
        characters = []
        for row in rows:
            character = {
                'id': row[0],
                'character_id': row[1],  # Le character_id est maintenant en position 1
                'alias': row[2],
                'alignment': row[3],
                'location': row[4],
                'origins': row[5],
                'role': row[6],
                'portrait_path': f"portraits/Portrait_{row[1]}.png"  # Chemin vers le portrait
            }
            # Ajouter origins2 si disponible (colonne 7)
            if len(row) > 7:
                character['origins2'] = row[7] if row[7] else None
            else:
                character['origins2'] = None
            
            # Ajouter tags si disponible (colonne 8)
            if len(row) > 8:
                character['tags'] = row[8] if row[8] else ""
            else:
                character['tags'] = ""
            
            characters.append(character)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "characters": characters
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/characters', methods=['POST'])
def create_character():
    """Crée un nouveau personnage"""
    try:
        data = request.get_json()
        
        # Valider les données requises
        required_fields = ['alias', 'alignment', 'location', 'origins', 'role']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({"error": f"Le champ '{field}' est requis"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # Vérifier que l'alias n'existe pas déjà
        cursor.execute("SELECT id FROM characters WHERE alias = ?", (data['alias'].strip(),))
        if cursor.fetchone():
            return jsonify({"error": "Un personnage avec ce nom existe déjà"}), 409
        
        # Insérer le nouveau personnage
        origins2 = data.get('origins2', '').strip() if data.get('origins2') else None
        tags = data.get('tags', '').strip() if data.get('tags') else ""
        
        cursor.execute("""
            INSERT INTO characters (alias, alignment, location, origins, role, origins2, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data['alias'].strip(),
            data['alignment'].strip(),
            data['location'].strip(),
            data['origins'].strip(),
            data['role'].strip(),
            origins2,
            tags
        ))
        
        character_id = cursor.lastrowid
        conn.commit()
        
        # Récupérer le personnage créé
        cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
        row = cursor.fetchone()
        
        new_character = {
            'id': row[0],
            'alias': row[1],
            'alignment': row[2],
            'location': row[3],
            'origins': row[4],
            'role': row[5],
            'origins2': row[6] if len(row) > 6 and row[6] else None,
            'tags': row[7] if len(row) > 7 and row[7] else ""
        }
        
        cursor.close()
        conn.close()
        
        print(f"✅ Nouveau personnage créé: {data['alias']} (ID: {character_id})")
        
        return jsonify({
            "message": f"Personnage '{data['alias']}' créé avec succès",
            "character": new_character
        }), 201
    
    except Exception as e:
        print(f"❌ Erreur create_character: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/random-character', methods=['GET'])
def get_random_character():
    """Récupère un personnage aléatoire pour le jeu"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM characters ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            character = {
                'id': row[0],
                'character_id': row[1],  # Le character_id est en position 1
                'alias': row[2],
                'alignment': row[3],
                'location': row[4],
                'origins': row[5],
                'role': row[6],
                'origins2': row[7] if len(row) > 7 and row[7] else None,
                'tags': row[8] if len(row) > 8 and row[8] else "",
                'portrait_path': f"portraits/Portrait_{row[1]}.png"  # Chemin vers le portrait
            }
        else:
            character = None
        
        cursor.close()
        conn.close()
        
        if character:
            return jsonify(dict(character))
        else:
            return jsonify({"error": "No characters found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/guess', methods=['POST'])
def check_guess():
    """Vérifie une tentative de devinette"""
    try:
        data = request.get_json()
        guessed_alias = data.get('character_name')  # Correspond à ce que le frontend envoie
        target_id = data.get('target_id')
        
        if not guessed_alias or not target_id:
            return jsonify({"error": "Missing character_name or target_id"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # Récupère le personnage deviné
        cursor.execute("SELECT * FROM characters WHERE alias = ?", (guessed_alias,))
        guessed_row = cursor.fetchone()
        
        # Récupère le personnage cible
        cursor.execute("SELECT * FROM characters WHERE id = ?", (target_id,))
        target_row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not guessed_row:
            return jsonify({"error": "Character not found"}), 404
        
        if not target_row:
            return jsonify({"error": "Target character not found"}), 404
        
        # Convertir les rows en dictionnaires
        guessed_char = {
            'id': guessed_row[0],
            'character_id': guessed_row[1],  # Le character_id est en position 1
            'alias': guessed_row[2],
            'alignment': guessed_row[3],
            'location': guessed_row[4],
            'origins': guessed_row[5],
            'role': guessed_row[6],
            'origins2': guessed_row[7] if len(guessed_row) > 7 and guessed_row[7] else None,
            'tags': guessed_row[8] if len(guessed_row) > 8 and guessed_row[8] else "",
            'portrait_path': f"portraits/Portrait_{guessed_row[1]}.png"
        }
        
        target_char = {
            'id': target_row[0],
            'character_id': target_row[1],  # Le character_id est en position 1
            'alias': target_row[2],
            'alignment': target_row[3],
            'location': target_row[4],
            'origins': target_row[5],
            'role': target_row[6],
            'origins2': target_row[7] if len(target_row) > 7 and target_row[7] else None,
            'tags': target_row[8] if len(target_row) > 8 and target_row[8] else ""
        }
        
        # Logique de comparaison
        result = {
            "success": True,
            "character": guessed_char,
            "correct": guessed_char['id'] == target_char['id'],
            "comparison": {
                "alignment": compare_attribute(guessed_char['alignment'], target_char['alignment']),
                "location": compare_attribute(guessed_char['location'], target_char['location']),
                "origins": compare_origins_combined(guessed_char['origins'], target_char['origins']),
                "role": compare_attribute(guessed_char['role'], target_char['role']),
                "tags": compare_tags(guessed_char['tags'], target_char['tags'])
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def compare_attribute(guessed, target):
    """Compare deux attributs simples"""
    if guessed == target:
        return "correct"  # Vert
    else:
        return "incorrect"  # Rouge

def compare_origins_combined(guess_origins, target_origins):
    """Compare les origines combinées (ex: 'Avengers, X-Men' vs 'X-Men, Cosmic')"""
    
    # Diviser les origines en ensembles
    guess_set = set(origin.strip() for origin in guess_origins.split(','))
    target_set = set(origin.strip() for origin in target_origins.split(','))
    
    if guess_set == target_set:
        return "correct"  # Vert - correspondance exacte
    elif guess_set & target_set:  # Intersection non vide
        return "partial"  # Jaune - correspondance partielle
    else:
        return "incorrect"  # Rouge - aucune correspondance

def compare_tags(guess_tags, target_tags):
    """Compare les tags (ex: 'Populaire, Mecha' vs 'Mecha, Avengers')"""
    
    # Gérer les cas où les tags sont vides ou None
    if not guess_tags:
        guess_tags = ""
    if not target_tags:
        target_tags = ""
    
    # Si les deux sont vides, c'est correct
    if not guess_tags.strip() and not target_tags.strip():
        return "correct"
    
    # Si l'un est vide et l'autre non, c'est incorrect
    if not guess_tags.strip() or not target_tags.strip():
        return "incorrect"
    
    # Diviser les tags en ensembles (séparés par virgules ou espaces)
    guess_set = set(tag.strip().lower() for tag in guess_tags.replace(',', ' ').split() if tag.strip())
    target_set = set(tag.strip().lower() for tag in target_tags.replace(',', ' ').split() if tag.strip())
    
    if guess_set == target_set:
        return "correct"  # Vert - correspondance exacte
    elif guess_set & target_set:  # Intersection non vide
        return "partial"  # Jaune - correspondance partielle
    else:
        return "incorrect"  # Rouge - aucune correspondance

@app.route('/api/search', methods=['GET'])
def search_characters():
    """Recherche de personnages pour l'autocomplete"""
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return jsonify([])
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT alias FROM characters WHERE alias LIKE ? ORDER BY alias LIMIT 10",
            (f'%{query}%',)
        )
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify([result[0] for result in results])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    """Met à jour les informations d'un personnage"""
    try:
        data = request.get_json()
        
        # Valider les données requises
        required_fields = ['alias', 'alignment', 'location', 'origins', 'role']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({"error": f"Le champ '{field}' est requis"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # Vérifier que le personnage existe
        cursor.execute("SELECT id FROM characters WHERE id = ?", (character_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Personnage non trouvé"}), 404
        
        # Mettre à jour le personnage
        origins2 = data.get('origins2', '').strip() if data.get('origins2') else None
        tags = data.get('tags', '').strip() if data.get('tags') else ""
        
        cursor.execute("""
            UPDATE characters 
            SET alias = ?, alignment = ?, location = ?, origins = ?, role = ?, origins2 = ?, tags = ?
            WHERE id = ?
        """, (
            data['alias'].strip(),
            data['alignment'].strip(),
            data['location'].strip(),
            data['origins'].strip(),
            data['role'].strip(),
            origins2,
            tags,
            character_id
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Personnage mis à jour avec succès"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    """Supprime un personnage"""
    print(f"🗑️ Requête DELETE reçue pour le personnage ID: {character_id}")
    
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Erreur: Connexion à la base de données échouée")
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # Vérifier que le personnage existe
        cursor.execute("SELECT alias FROM characters WHERE id = ?", (character_id,))
        character = cursor.fetchone()
        if not character:
            print(f"❌ Personnage ID {character_id} non trouvé")
            return jsonify({"error": "Personnage non trouvé"}), 404
        
        character_name = character[0]
        print(f"✅ Personnage trouvé: {character_name}")
        
        # Supprimer le personnage (les tags seront supprimés automatiquement grâce à ON DELETE CASCADE)
        cursor.execute("DELETE FROM characters WHERE id = ?", (character_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Personnage '{character_name}' supprimé avec succès")
        
        return jsonify({"message": f"Personnage '{character_name}' supprimé avec succès"}), 200
    
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
