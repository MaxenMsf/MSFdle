#!/usr/bin/env python3
"""
Version simplifiée de l'API MSFdle pour diagnostic
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'msfdle.db')

@app.route('/')
def home():
    return jsonify({
        "message": "MSFdle API - Version de test",
        "status": "running",
        "database": os.path.exists(DATABASE_PATH)
    })

@app.route('/test')
def test():
    """Test simple de l'API"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "status": "success",
            "characters_count": count,
            "database_path": DATABASE_PATH
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "database_path": DATABASE_PATH
        }), 500

@app.route('/characters')
def get_characters():
    """Récupère tous les personnages"""
    try:
        print(f"📁 Tentative de connexion à: {DATABASE_PATH}")
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Utiliser la vue character_with_tags qui contient tous les tags
        cursor = conn.cursor()
        cursor.execute("SELECT id, alias, alignment, location, origins, role, tags FROM character_with_tags ORDER BY alias")
        rows = cursor.fetchall()
        
        characters = []
        for row in rows:
            # Séparer les nouveaux tags des tags de base (role, alignment, location)
            all_tags = row[6] if row[6] else ""  # tags de la vue
            role = row[5]  # role
            alignment = row[2]  # alignment
            location = row[3]  # location
            
            # Tags de base à exclure (correspondant aux autres colonnes)
            base_tags = {role, alignment, location}
            
            # Filtrer pour garder seulement les nouveaux tags thématiques
            interesting_tags = []
            if all_tags:
                for tag in all_tags.split(', '):
                    tag = tag.strip()
                    if tag and tag not in base_tags:
                        interesting_tags.append(tag)
            
            final_tags = ', '.join(interesting_tags) if interesting_tags else 'Aucun'
            print(f"🏷️ {row[1]}: tags_bruts='{all_tags}' -> tags_intéressants='{final_tags}'")
            
            characters.append({
                'id': row[0],  # id
                'name': row[1],  # alias (Personnage)
                'alignment': row[2],  # alignment (Affiliation: Hero/Vilain) 
                'origins': row[4],  # origins (Origine)
                'location': row[3],  # location (Secteur: Ville/Mondial/Cosmique)
                'role': row[5],  # role (Rôle: Cogneur/Tireur/etc)
                'tags': final_tags  # Tags uniquement
            })
        
        conn.close()
        print(f"✅ {len(characters)} personnages récupérés")
        return jsonify(characters)
        
    except Exception as e:
        print(f"❌ Erreur dans get_characters: {e}")
        return jsonify({
            "error": str(e),
            "database_path": DATABASE_PATH,
            "database_exists": os.path.exists(DATABASE_PATH)
        }), 500

@app.route('/random_character')
def get_random_character():
    """Récupère un personnage aléatoire"""
    try:
        print(f"🎲 Récupération personnage aléatoire")
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, alias, alignment, location, origins, role, tags FROM character_with_tags ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            # Même logique pour le personnage aléatoire
            all_tags = row[6] if row[6] else ""
            role = row[5]
            alignment = row[2]
            location = row[3]
            
            # Tags de base à exclure
            base_tags = {role, alignment, location}
            
            interesting_tags = []
            if all_tags:
                for tag in all_tags.split(', '):
                    tag = tag.strip()
                    if tag and tag not in base_tags:
                        interesting_tags.append(tag)
            
            character = {
                'id': row[0],  # id
                'name': row[1],  # alias (Personnage)
                'alignment': row[2],  # alignment (Affiliation)
                'origins': row[4],  # origins (Origine)
                'location': row[3],  # location (Secteur)
                'role': row[5],  # role (Rôle)
                'tags': ', '.join(interesting_tags) if interesting_tags else 'Aucun'  # Tags uniquement
            }
            print(f"✅ Personnage trouvé: {character['name']}")
        else:
            character = {"error": "Aucun personnage trouvé"}
        
        conn.close()
        return jsonify(character)
        
    except Exception as e:
        print(f"❌ Erreur dans get_random_character: {e}")
        return jsonify({
            "error": str(e),
            "database_path": DATABASE_PATH
        }), 500

def compare_attribute(guessed, target):
    """Compare deux attributs simples"""
    print(f"🔍 Comparaison attribut: '{guessed}' vs '{target}'")
    if str(guessed).strip() == str(target).strip():
        print("✅ Attribut correct")
        return "correct"  # Vert
    else:
        print("❌ Attribut incorrect")
        return "incorrect"  # Rouge

def compare_origins_combined(guess_origins, target_origins):
    """Compare les origines combinées avec support partiel"""
    print(f"🔍 Comparaison origines: '{guess_origins}' vs '{target_origins}'")
    
    if not guess_origins or not target_origins:
        return "incorrect"
    
    # Nettoyer et séparer les origines
    guess_parts = [part.strip() for part in str(guess_origins).split(',') if part.strip()]
    target_parts = [part.strip() for part in str(target_origins).split(',') if part.strip()]
    
    guess_set = set(guess_parts)
    target_set = set(target_parts)
    
    print(f"📊 Guess set: {guess_set}, Target set: {target_set}")
    
    if guess_set == target_set:
        print("✅ Origines identiques -> correct")
        return "correct"  # Correspondance exacte
    elif guess_set & target_set:  # Intersection non vide
        print("🟡 Origines partielles -> partial")
        return "partial"  # Correspondance partielle
    else:
        print("❌ Aucune correspondance -> incorrect")
        return "incorrect"

def compare_tags(guess_tags, target_tags):
    """Compare les tags"""
    # Gérer les cas où les tags sont vides ou None
    if not guess_tags:
        guess_tags = ""
    if not target_tags:
        target_tags = ""
    
    # Si les deux sont vides, c'est correct
    if not str(guess_tags).strip() and not str(target_tags).strip():
        return "correct"
    
    # Diviser les tags en ensembles (séparés par virgules)
    guess_set = set(tag.strip().lower() for tag in str(guess_tags).split(',') if tag.strip())
    target_set = set(tag.strip().lower() for tag in str(target_tags).split(',') if tag.strip())
    
    if guess_set == target_set:
        return "correct"  # Vert - correspondance exacte
    elif guess_set & target_set:  # Intersection non vide
        return "partial"  # Jaune - correspondance partielle
    else:
        return "incorrect"  # Rouge - aucune correspondance

@app.route('/compare', methods=['POST'])
def compare_guess():
    """Compare un personnage deviné avec le personnage cible"""
    try:
        data = request.get_json()
        guessed_id = data.get('guess_id')
        target_id = data.get('target_id')
        
        print(f"🔍 Comparaison: ID {guessed_id} vs ID {target_id}")
        print(f"📦 Données reçues: {data}")
        
        if not guessed_id or not target_id:
            return jsonify({"error": "Missing guess_id or target_id"}), 400
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Récupérer le personnage deviné par ID
        cursor.execute("SELECT id, alias, alignment, location, origins, role, tags FROM character_with_tags WHERE id = ?", (guessed_id,))
        guessed_row = cursor.fetchone()
        
        # Récupérer le personnage cible par ID  
        cursor.execute("SELECT id, alias, alignment, location, origins, role, tags FROM character_with_tags WHERE id = ?", (target_id,))
        target_row = cursor.fetchone()
        
        conn.close()
        
        if not guessed_row:
            return jsonify({"error": f"Character with ID '{guessed_id}' not found"}), 404
        
        if not target_row:
            return jsonify({"error": f"Target character with ID '{target_id}' not found"}), 404
        
        # Convertir en dictionnaires avec la bonne structure
        guessed_all_tags = guessed_row[6] if guessed_row[6] else ""
        guessed_role = guessed_row[5]
        guessed_alignment = guessed_row[2]
        guessed_location = guessed_row[3]
        
        # Tags de base à exclure pour guessed
        guessed_base_tags = {guessed_role, guessed_alignment, guessed_location}
        
        guessed_interesting_tags = []
        if guessed_all_tags:
            for tag in guessed_all_tags.split(', '):
                tag = tag.strip()
                if tag and tag not in guessed_base_tags:
                    guessed_interesting_tags.append(tag)
        
        target_all_tags = target_row[6] if target_row[6] else ""
        target_role = target_row[5]
        target_alignment = target_row[2]
        target_location = target_row[3]
        
        # Tags de base à exclure pour target
        target_base_tags = {target_role, target_alignment, target_location}
        
        target_interesting_tags = []
        if target_all_tags:
            for tag in target_all_tags.split(', '):
                tag = tag.strip()
                if tag and tag not in target_base_tags:
                    target_interesting_tags.append(tag)
        
        guessed_char = {
            'id': guessed_row[0],
            'name': guessed_row[1],  # Personnage
            'alignment': guessed_row[2],  # Affiliation (Hero/Vilain)
            'origins': guessed_row[4],  # Origine
            'location': guessed_row[3],  # Secteur (Ville/Mondial/Cosmique)
            'role': guessed_row[5],  # Rôle (Cogneur/Tireur/etc)
            'tags': ', '.join(guessed_interesting_tags) if guessed_interesting_tags else 'Aucun'  # Tags uniquement
        }
        
        target_char = {
            'id': target_row[0],
            'name': target_row[1],  # Personnage
            'alignment': target_row[2],  # Affiliation (Hero/Vilain)
            'origins': target_row[4],  # Origine
            'location': target_row[3],  # Secteur (Ville/Mondial/Cosmique)
            'role': target_row[5],  # Rôle (Cogneur/Tireur/etc)
            'tags': ', '.join(target_interesting_tags) if target_interesting_tags else 'Aucun'  # Tags uniquement
        }
        
        # Logique de comparaison avec logs détaillés
        print(f"🎯 Comparaison entre:")
        print(f"   Deviné: {guessed_char}")
        print(f"   Cible:  {target_char}")
        
        comparison_result = {
            "alignment": compare_attribute(guessed_char['alignment'], target_char['alignment']),  # Affiliation
            "location": compare_attribute(guessed_char['location'], target_char['location']),  # Secteur  
            "origins": compare_origins_combined(guessed_char['origins'], target_char['origins']),  # Origine
            "role": compare_attribute(guessed_char['role'], target_char['role']),  # Rôle
            "tags": compare_tags(guessed_char['tags'], target_char['tags'])  # Tags
        }
        
        print(f"📊 Résultats de comparaison: {comparison_result}")
        
        result = {
            "character": guessed_char,
            "correct": guessed_char['id'] == target_char['id'],
            "comparison": comparison_result
        }
        
        print(f"✅ Comparaison réussie: {result['correct']}")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Erreur dans compare_guess: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Démarrage de l'API MSFdle (version test)")
    print(f"📁 Base de données: {DATABASE_PATH}")
    print(f"📁 Existe: {os.path.exists(DATABASE_PATH)}")
    
    app.run(debug=True, port=5001, host='127.0.0.1')
