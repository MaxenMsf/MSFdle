#!/usr/bin/env python3
"""
Test des correspondances de tags pour vérifier les couleurs
"""

# Exemples de tests pour les correspondances de tags

test_cases = [
    {
        "name": "Correspondance exacte (VERT)",
        "guess": "SPIDER-VERSE, SINISTER SIX",
        "target": "SPIDER-VERSE, SINISTER SIX",
        "expected": "correct"
    },
    {
        "name": "Correspondance partielle (JAUNE)",
        "guess": "SPIDER-VERSE, X-FORCE",
        "target": "SPIDER-VERSE, SINISTER SIX", 
        "expected": "partial"
    },
    {
        "name": "Aucune correspondance (ROUGE)",
        "guess": "X-FORCE, SECRET WARRIOR",
        "target": "SPIDER-VERSE, SINISTER SIX",
        "expected": "incorrect"
    },
    {
        "name": "Tous deux AUCUN (VERT)",
        "guess": "AUCUN",
        "target": "AUCUN",
        "expected": "correct"
    },
    {
        "name": "L'un a des tags, l'autre AUCUN (ROUGE)",
        "guess": "SPIDER-VERSE",
        "target": "AUCUN",
        "expected": "incorrect"
    }
]

def compare_tags_test(guess_tags, target_tags):
    """Fonction de test pour compare_tags"""
    
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
    print("🧪 Test des correspondances de tags")
    print("=" * 50)
    
    for test in test_cases:
        result = compare_tags_test(test["guess"], test["target"])
        status = "✅" if result == test["expected"] else "❌"
        
        print(f"{status} {test['name']}")
        print(f"   Deviné: '{test['guess']}'")
        print(f"   Cible:  '{test['target']}'")
        print(f"   Résultat: {result} (attendu: {test['expected']})")
        print()
    
    print("🎨 Correspondances de couleurs:")
    print("   🟢 VERT (correct) = Correspondance exacte")
    print("   🟡 JAUNE (partial) = Correspondance partielle")  
    print("   🔴 ROUGE (incorrect) = Aucune correspondance")