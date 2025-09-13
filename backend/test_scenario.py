#!/usr/bin/env python3
"""
Test complet du scénario Adam Warlock vs Docteur Fatalis
"""

# Données réelles de la base
adam_warlock = {
    'id': 181,
    'alias': 'Adam Warlock',
    'alignment': 'Hero',
    'location': 'Cosmique',
    'origins': 'Mystique',
    'role': 'Soutien',
    'tags': 'INFINITY WATCH'
}

docteur_fatalis = {
    'id': 189,
    'alias': 'Docteur fatalis',
    'alignment': 'Vilain',
    'location': 'Mondial',
    'origins': 'Mystique, Techno',
    'role': 'Manipulateur',
    'tags': 'AUCUN'
}

def compare_attribute(guessed, target):
    """Compare deux attributs simples"""
    if guessed == target:
        return "correct"  # Vert
    else:
        return "incorrect"  # Rouge

def compare_origins_advanced(guess_origins, target_origins):
    """Compare les origines avec logique améliorée pour correspondances partielles"""
    
    # Nettoyer et normaliser les chaînes
    if not guess_origins:
        guess_origins = ""
    if not target_origins:
        target_origins = ""
    
    # Si identiques, c'est correct
    if guess_origins.strip() == target_origins.strip():
        return "correct"
    
    # Diviser les origines en ensembles
    guess_set = set(origin.strip() for origin in guess_origins.split(',') if origin.strip())
    target_set = set(origin.strip() for origin in target_origins.split(',') if origin.strip())
    
    # Correspondance exacte des ensembles
    if guess_set == target_set:
        return "correct"  # Vert - correspondance exacte
    
    # Correspondance partielle (au moins une origine commune)
    elif guess_set & target_set:  # Intersection non vide
        return "partial"  # Jaune - correspondance partielle
    
    # Aucune correspondance
    else:
        return "incorrect"  # Rouge - aucune correspondance

def compare_tags(guess_tags, target_tags):
    """Compare les tags"""
    
    # Gérer les cas où les tags sont vides ou None
    if not guess_tags:
        guess_tags = ""
    if not target_tags:
        target_tags = ""
    
    # Cas spéciaux pour "AUCUN"
    if guess_tags.strip() == "AUCUN" and target_tags.strip() == "AUCUN":
        return "correct"  # Vert - les deux n'ont aucun tag
    
    if guess_tags.strip() == "AUCUN" or target_tags.strip() == "AUCUN":
        return "incorrect"  # Rouge - l'un a des tags, l'autre non
    
    # Si les deux sont vides (ne devrait pas arriver avec la logique AUCUN)
    if not guess_tags.strip() and not target_tags.strip():
        return "correct"
    
    # Si l'un est vide et l'autre non, c'est incorrect
    if not guess_tags.strip() or not target_tags.strip():
        return "incorrect"
    
    # Diviser les tags en ensembles (séparés par virgules)
    guess_set = set(tag.strip() for tag in guess_tags.split(',') if tag.strip())
    target_set = set(tag.strip() for tag in target_tags.split(',') if tag.strip())
    
    if guess_set == target_set:
        return "correct"  # Vert - correspondance exacte
    elif guess_set & target_set:  # Intersection non vide
        return "partial"  # Jaune - correspondance partielle
    else:
        return "incorrect"  # Rouge - aucune correspondance

if __name__ == "__main__":
    print("🎯 Test complet: Docteur fatalis deviné quand Adam Warlock est la cible")
    print("=" * 70)
    
    # Simulation: Docteur fatalis deviné, Adam Warlock est la cible
    guessed_char = docteur_fatalis
    target_char = adam_warlock
    
    comparison = {
        "alignment": compare_attribute(guessed_char['alignment'], target_char['alignment']),
        "location": compare_attribute(guessed_char['location'], target_char['location']),
        "origins": compare_origins_advanced(guessed_char['origins'], target_char['origins']),
        "role": compare_attribute(guessed_char['role'], target_char['role']),
        "tags": compare_tags(guessed_char['tags'], target_char['tags'])
    }
    
    print(f"Personnage deviné: {guessed_char['alias']}")
    print(f"Personnage cible: {target_char['alias']}")
    print()
    
    print("📊 Résultats de comparaison:")
    print(f"   Affiliation: {guessed_char['alignment']} vs {target_char['alignment']} → {comparison['alignment']} {'🔴' if comparison['alignment'] == 'incorrect' else '🟢'}")
    print(f"   Secteur:     {guessed_char['location']} vs {target_char['location']} → {comparison['location']} {'🔴' if comparison['location'] == 'incorrect' else '🟢'}")
    print(f"   Origine:     '{guessed_char['origins']}' vs '{target_char['origins']}' → {comparison['origins']} {'🟡' if comparison['origins'] == 'partial' else '🔴' if comparison['origins'] == 'incorrect' else '🟢'}")
    print(f"   Rôle:        {guessed_char['role']} vs {target_char['role']} → {comparison['role']} {'🔴' if comparison['role'] == 'incorrect' else '🟢'}")
    print(f"   Tags:        '{guessed_char['tags']}' vs '{target_char['tags']}' → {comparison['tags']} {'🔴' if comparison['tags'] == 'incorrect' else '🟢'}")
    
    print()
    print("✅ Résultat attendu: Origine devrait être 🟡 JAUNE (partial) car 'Mystique' est commun")
    print("✅ Autres colonnes: 🔴 ROUGE (incorrect) car aucune correspondance")