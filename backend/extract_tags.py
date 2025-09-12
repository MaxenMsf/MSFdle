#!/usr/bin/env python3
"""
Extracteur de tags depuis les captures d'écran MSF
Analyse les captures d'écran et extrait les tags des personnages
"""

import sys
import os

# Ajouter le répertoire data au path pour importer character_tags
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

try:
    from character_tags import IGNORED_TAGS
except ImportError:
    print("❌ Erreur: Impossible d'importer character_tags.py")
    sys.exit(1)

def extract_tags_from_screenshots():
    """
    Analyse les captures d'écran fournies par l'utilisateur
    """
    print("🔍 Analyse des captures d'écran MSF")
    print("=" * 50)
    
    # Basé sur vos captures d'écran, voici les tags que j'ai identifiés:
    
    screenshots_analysis = {
        "Phantom Rider": {
            "character_id": "PhantomRider",  # À vérifier dans votre CSV
            "visible_tags": ["HÉROS", "VILLE", "MYSTIQUE", "TIREUR", "SECRET WARRIOR"],
            "filtered_tags": ["SECRET WARRIOR"]  # Après filtrage des tags ignorés
        },
        
        "Scorpion": {
            "character_id": "Scorpion", 
            "visible_tags": ["SUPER-VILAIN", "VILLE", "TECHNO", "COGNEUR", "SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX", "INFESTATION", "CHAPITRE 2 - CONQUÉRANT"],
            "filtered_tags": ["SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX", "INFESTATION"]
        },
        
        "Spider-Man Supérieur": {
            "character_id": "SuperiorSpiderMan",
            "visible_tags": ["SUPER-VILAIN", "VILLE", "TECHNO", "SOUTIEN", "SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX", "SUPERIOR SIX", "CHAPITRE 2 - CONQUÉRANT"],
            "filtered_tags": ["SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX", "SUPERIOR SIX"]
        },
        
        "Super-Bouffon": {
            "character_id": "Hobgoblin",
            "visible_tags": ["SUPER-VILAIN", "VILLE", "TECHNO", "MANIPULATEUR", "SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX", "CHAPITRE 2 - CONQUÉRANT"],
            "filtered_tags": ["SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX"]
        },
        
        "Domino": {
            "character_id": "Domino",
            "visible_tags": ["HÉROS", "MONDIAL", "MUTANT", "MANIPULATEUR", "X-FORCE", "SECRET WARRIOR", "DEADPOOL ET SES COPAINS"],
            "filtered_tags": ["X-FORCE"]
        },
        
        "Negasonic": {
            "character_id": "Negasonic",
            "visible_tags": ["HÉROS", "MONDIAL", "MUTANT", "TIREUR", "X-FORCE", "SECRET WARRIOR", "PLEIN D'ÉNERGIE", "DEADPOOL ET SES COPAINS"],
            "filtered_tags": ["X-FORCE"]
        },
        
        "Quake": {
            "character_id": "Quake",
            "visible_tags": ["HÉROS", "MONDIAL", "BIOTECHNIQUE", "MANIPULATEUR", "S.H.I.E.L.D", "INHUMAN", "SECRET WARRIOR"],
            "filtered_tags": ["S.H.I.E.L.D", "INHUMAN"]
        },
        
        "Shocker": {
            "character_id": "Shocker",
            "visible_tags": ["SUPER-VILAIN", "VILLE", "TECHNO", "TIREUR", "SPIDER-VERSE", "SINISTER SIX", "CHAPITRE 2 - CONQUÉRANT"],
            "filtered_tags": ["SPIDER-VERSE", "SINISTER SIX"]
        },
        
        "Vautour": {
            "character_id": "Vulture",
            "visible_tags": ["SUPER-VILAIN", "VILLE", "TECHNO", "COGNEUR", "SPIDER-VERSE", "SINISTER SIX", "CHAPITRE 2 - CONQUÉRANT"],
            "filtered_tags": ["SPIDER-VERSE", "SINISTER SIX"]
        },
        
        "Yo-Yo": {
            "character_id": "YoYo",
            "visible_tags": ["HÉROS", "MONDIAL", "BIOTECHNIQUE", "PROTECTEUR", "S.H.I.E.L.D", "INHUMAN", "SECRET WARRIOR"],
            "filtered_tags": ["S.H.I.E.L.D", "INHUMAN"]
        },
        
        "Abomination": {
            "character_id": "Abomination",
            "visible_tags": ["SUPER-VILAIN", "MONDIAL", "BIOTECHNIQUE", "COGNEUR", "GAMMA"],
            "filtered_tags": ["GAMMA"]
        },
        
        "Adam Warlock": {
            "character_id": "AdamWarlock",
            "visible_tags": ["HÉROS", "COSMIQUE", "MYSTIQUE", "SOUTIEN", "INFINITY WATCH", "LÉGENDAIRE"],
            "filtered_tags": ["INFINITY WATCH"]
        }
    }
    
    return screenshots_analysis

def filter_tags(visible_tags):
    """
    Filtre les tags en supprimant ceux de la liste IGNORED_TAGS
    """
    filtered = []
    for tag in visible_tags:
        # Normaliser les comparaisons (supprimer les accents, casse, etc.)
        tag_normalized = tag.upper().replace("É", "E").replace("È", "E").replace("Ê", "E")
        
        is_ignored = False
        for ignored_tag in IGNORED_TAGS:
            ignored_normalized = ignored_tag.upper().replace("É", "E").replace("È", "E").replace("Ê", "E")
            if tag_normalized == ignored_normalized:
                is_ignored = True
                break
        
        if not is_ignored:
            filtered.append(tag)
    
    return filtered

def generate_character_tags():
    """
    Génère le dictionnaire character_tags basé sur l'analyse des captures
    """
    analysis = extract_tags_from_screenshots()
    
    character_tags = {}
    all_tags = set()
    
    print("🏷️ Tags extraits des captures d'écran:")
    print("-" * 50)
    
    for character_name, data in analysis.items():
        character_id = data["character_id"]
        visible_tags = data["visible_tags"]
        
        # Filtrer les tags
        filtered_tags = filter_tags(visible_tags)
        
        if filtered_tags:
            character_tags[character_id] = filtered_tags
            all_tags.update(filtered_tags)
            
            print(f"✅ {character_name} ({character_id}):")
            print(f"   Visible: {', '.join(visible_tags)}")
            print(f"   Gardés:  {', '.join(filtered_tags)}")
        else:
            print(f"⚪ {character_name} ({character_id}): Aucun tag gardé après filtrage")
        print()
    
    available_tags = sorted(list(all_tags))
    
    print(f"📊 Résumé:")
    print(f"   - Personnages analysés: {len(analysis)}")
    print(f"   - Personnages avec tags: {len(character_tags)}")
    print(f"   - Tags uniques extraits: {len(available_tags)}")
    print(f"   - Tags: {', '.join(available_tags)}")
    
    return character_tags, available_tags

def update_character_tags_file():
    """
    Met à jour le fichier character_tags.py avec les tags extraits
    """
    character_tags, available_tags = generate_character_tags()
    
    # Lire le fichier actuel
    tags_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'character_tags.py')
    
    with open(tags_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les sections character_tags et available_tags
    import re
    
    # Mise à jour de character_tags
    character_tags_str = "character_tags = {\n"
    for char_id, tags in character_tags.items():
        tags_formatted = ', '.join([f'"{tag}"' for tag in tags])
        character_tags_str += f'    "{char_id}": [{tags_formatted}],\n'
    character_tags_str += "}"
    
    # Mise à jour de available_tags  
    available_tags_str = "available_tags = [\n"
    for tag in available_tags:
        available_tags_str += f'    "{tag}",\n'
    available_tags_str += "]"
    
    # Remplacer dans le contenu
    content = re.sub(
        r'character_tags = \{[^}]*\}', 
        character_tags_str, 
        content, 
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'available_tags = \[[^\]]*\]', 
        available_tags_str, 
        content, 
        flags=re.DOTALL
    )
    
    # Écrire le fichier mis à jour
    with open(tags_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Fichier {tags_file_path} mis à jour!")
    
    return character_tags, available_tags

if __name__ == "__main__":
    print("🎮 Extracteur de Tags MSFdle")
    print("=" * 50)
    
    # Extraire et mettre à jour les tags
    character_tags, available_tags = update_character_tags_file()
    
    print(f"\n🎉 Extraction terminée!")
    print(f"📁 Prochaine étape: Exécuter 'python apply_tags.py' pour appliquer à la base de données")