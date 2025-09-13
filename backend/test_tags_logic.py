#!/usr/bin/env python3
"""
Test de la logique de comparaison des tags
"""

def compare_tags(guess_tags, target_tags):
    """Compare les tags (ex: 'SPIDER-VERSE, SINISTER SIX' vs 'SINISTER SIX, X-FORCE')"""
    
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
    print("🧪 Test de la logique de comparaison des tags")
    print("=" * 50)
    
    # Test avec Scorpion vs Bouffon rouge (selon votre capture)
    scorpion_tags = "INFESTATION, INSIDIOUS SIX, SINISTER SIX, SPIDER-VERSE"
    bouffon_rouge_tags = "SPIDER-VERSE, CONSCIENCE COLLECTIVE, SYMBIOTE"
    
    result = compare_tags(scorpion_tags, bouffon_rouge_tags)
    print(f"Scorpion: {scorpion_tags}")
    print(f"Bouffon rouge: {bouffon_rouge_tags}")
    print(f"Résultat: {result}")
    print()
    
    # Intersection attendue: SPIDER-VERSE
    scorpion_set = set(tag.strip() for tag in scorpion_tags.split(','))
    bouffon_set = set(tag.strip() for tag in bouffon_rouge_tags.split(','))
    intersection = scorpion_set & bouffon_set
    print(f"Tags en commun: {intersection}")
    print(f"Devrait être 'partial': {result == 'partial'}")