#!/usr/bin/env python3
"""
Test de la nouvelle logique de comparaison des origines
"""

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

# Test avec les données réelles
test_cases = [
    {
        "name": "Adam Warlock vs Docteur Fatalis (Mystique en commun)",
        "guess": "Mystique",  # Adam Warlock
        "target": "Mystique, Techno",  # Docteur Fatalis
        "expected": "partial"  # Devrait être JAUNE
    },
    {
        "name": "Même origines exactes",
        "guess": "Mystique, Techno",
        "target": "Mystique, Techno",
        "expected": "correct"  # Devrait être VERT
    },
    {
        "name": "Aucune correspondance",
        "guess": "Biotechnique",
        "target": "Mystique, Techno",
        "expected": "incorrect"  # Devrait être ROUGE
    },
    {
        "name": "Correspondance partielle inversée",
        "guess": "Mystique, Techno",  # Docteur Fatalis
        "target": "Mystique",  # Adam Warlock
        "expected": "partial"  # Devrait être JAUNE
    }
]

if __name__ == "__main__":
    print("🧪 Test de la logique des origines")
    print("=" * 50)
    
    for test in test_cases:
        result = compare_origins_advanced(test["guess"], test["target"])
        status = "✅" if result == test["expected"] else "❌"
        
        print(f"{status} {test['name']}")
        print(f"   Deviné: '{test['guess']}'")
        print(f"   Cible:  '{test['target']}'")
        print(f"   Résultat: {result} (attendu: {test['expected']})")
        print()
    
    print("🎨 Correspondances attendues:")
    print("   🟢 VERT (correct) = Origines identiques")
    print("   🟡 JAUNE (partial) = Au moins une origine commune")  
    print("   🔴 ROUGE (incorrect) = Aucune origine commune")