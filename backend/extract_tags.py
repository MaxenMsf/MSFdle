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
    Extrait les tags des personnages visibles dans les captures
    """
    print("🔍 Analyse des captures d'écran MSF")
    print("=" * 50)
    
    # Basé sur vos captures d'écran, voici tous les tags que j'ai identifiés:
    screenshots_analysis = {
        # ===== PERSONNAGES DES CAPTURES D'ÉCRAN =====
        
        "Essaim": {
            "character_id": "Swarm",
            "visible_tags": ["SUPER-VILAIN", "VILLE", "BIOTECHNIQUE", "MANIPULATEUR", "SPIDER-VERSE", "SINISTER SIX", "INFESTATION"],
            "filtered_tags": ["SPIDER-VERSE", "SINISTER SIX", "INFESTATION"]
        },
        
        "Factionnaire de la Main": {
            "character_id": "HandTank_Stealth",
            "visible_tags": ["SUPER-VILAIN", "VILLE", "MYSTIQUE", "PROTECTEUR", "MAIN", "SERVITEUR"],
            "filtered_tags": ["MAIN", "SERVITEUR"]
        },
        
        "Falcon": {
            "character_id": "Falcon",
            "visible_tags": ["HÉROS", "MONDIAL", "TECHNO", "TIREUR", "TECHNO-ARMURE", "MIGHTY AVENGERS", "UNCANNY AVENGERS", "JUNETEENTH"],
            "filtered_tags": ["TECHNO-ARMURE", "MIGHTY AVENGERS", "UNCANNY AVENGERS", "JUNETEENTH"]
        },
        
        "Falcon (Joaquin)": {
            "character_id": "FalconJoaquin",
            "visible_tags": ["HÉROS", "MONDIAL", "TECHNO", "SOUTIEN", "LIBERTÉ", "ÉLITES DE L'ANNIVERSAIRE"],
            "filtered_tags": ["LIBERTÉ"]
        },
        
        "Fantassin du S.H.I.E.L.D.": {
            "character_id": "ShieldDmg_Defense",
            "visible_tags": ["HÉROS", "MONDIAL", "EXPERTISE", "TIREUR", "S.H.I.E.L.D", "SERVITEUR"],
            "filtered_tags": ["S.H.I.E.L.D", "SERVITEUR"]
        },
        
        "Fantôme": {
            "character_id": "Ghost",
            "visible_tags": ["SUPER-VILAIN", "MONDIAL", "BIOTECHNIQUE", "TECHNO", "MANIPULATEUR", "PYM TECH", "THUNDERBOLT", "CHAPITRE 1 - ANNONCIATEUR"],
            "filtered_tags": ["PYM TECH", "THUNDERBOLT"]
        },
        
        "Fantomex": {
            "character_id": "Fantomex",
            "visible_tags": ["HÉROS", "MONDIAL", "MUTANT", "TIREUR", "UNLIMITED X-MEN"],
            "filtered_tags": ["UNLIMITED X-MEN"]
        },
        
        "Faucheuse Kree": {
            "character_id": "KreeDmg_Speed",
            "visible_tags": ["SUPER-VILAIN", "COSMIQUE", "BIOTECHNIQUE", "COGNEUR", "KREE", "SERVITEUR"],
            "filtered_tags": ["KREE", "SERVITEUR"]
        },
        
        "Fauve": {
            "character_id": "Beast",
            "visible_tags": ["HÉROS", "MONDIAL", "MUTANT", "SOUTIEN", "UNCANNY X-MEN", "ASTONISHING X-MEN", "IMMORTAL X-MEN", "UNCANNY AVENGERS", "ÉLITES DE L'ANNIVERSAIRE"],
            "filtered_tags": ["UNCANNY X-MEN", "ASTONISHING X-MEN", "IMMORTAL X-MEN", "UNCANNY AVENGERS"]
        },
        
        "Fauve noir": {
            "character_id": "DarkBeast",
            "visible_tags": ["SUPER-VILAIN", "MONDIAL", "MUTANT", "MANIPULATEUR", "GRAINE DE MORT"],
            "filtered_tags": ["GRAINE DE MORT"]
        },
        
        "Femme invisible": {
            "character_id": "InvisibleWoman",
            "visible_tags": ["HÉROS", "COSMIQUE", "BIOTECHNIQUE", "PROTECTEUR", "QUATRE FANTASTIQUES", "MIGHTY AVENGERS", "LÉGENDAIRE", "LE CASSE DE NULLE-PART", "PLEIN D'ÉNERGIE", "MÈRES MARVEL", "EN COUPLE"],
            "filtered_tags": ["QUATRE FANTASTIQUES", "MIGHTY AVENGERS", "LE CASSE DE NULLE-PART", "MÈRES MARVEL"]
        },
        
        "Femme invisible (MCU)": {
            "character_id": "InvisibleWomanMCU",
            "visible_tags": ["HÉROS", "COSMIQUE", "BIOTECHNIQUE", "COGNEUR", "QUATRE FANTASTIQUES (MCU)", "CHAPITRE 1 - ANNONCIATEUR", "CHAPITRE 2 - CONQUÉRANT"],
            "filtered_tags": ["QUATRE FANTASTIQUES (MCU)"]
        },
        
        "Feu du soleil": {
            "character_id": "Sunfire",
            "visible_tags": ["HÉROS", "MONDIAL", "MUTANT", "TIREUR", "UNLIMITED X-MEN", "DIVISION ALPHA"],
            "filtered_tags": ["UNLIMITED X-MEN", "DIVISION ALPHA"]
        },
        
        "Firestar": {
            "character_id": "Firestar",
            "visible_tags": ["HÉROS", "VILLE", "MUTANT", "TIREUR", "NEW WARRIOR"],
            "filtered_tags": ["NEW WARRIOR"]
        },
        
        "Forge": {
            "character_id": "Forge",
            "visible_tags": ["HÉROS", "MONDIAL", "MUTANT", "SOUTIEN", "X-TREME X-MEN"],
            "filtered_tags": ["X-TREME X-MEN"]
        },
        
        "Franklin Richards": {
            "character_id": "FranklinRichards",
            "visible_tags": ["HÉROS", "COSMIQUE", "BIOTECHNIQUE", "MANIPULATEUR", "QUATRE FANTASTIQUES (MCU)", "CHAPITRE 1 - ANNONCIATEUR", "CHAPITRE 2 - CONQUÉRANT"],
            "filtered_tags": ["QUATRE FANTASTIQUES (MCU)"]
        },
        
        "Fusilier d'Hydra": {
            "character_id": "HydraDmg_Buff",
            "visible_tags": ["SUPER-VILAIN", "MONDIAL", "TECHNO", "TIREUR", "HYDRA", "SERVITEUR"],
            "filtered_tags": ["HYDRA", "SERVITEUR"]
        },
        
        "Gambit": {
            "character_id": "Gambit",
            "visible_tags": ["HÉROS", "MONDIAL", "MUTANT", "TIREUR", "UNLIMITED X-MEN", "X-TREME X-MEN", "EN COUPLE"],
            "filtered_tags": ["UNLIMITED X-MEN", "X-TREME X-MEN"]
        },
        
        "Gamora": {
            "character_id": "Gamora",
            "visible_tags": ["HÉROS", "COSMIQUE", "EXPERTISE", "COGNEUR", "GARDIEN", "INFINITY WATCH"],
            "filtered_tags": ["GARDIEN", "INFINITY WATCH"]
        },
        
        "Garde cuirassé d'Hydra": {
            "character_id": "HydraTank_Taunt",
            "visible_tags": ["SUPER-VILAIN", "MONDIAL", "TECHNO", "PROTECTEUR", "HYDRA", "SERVITEUR"],
            "filtered_tags": ["HYDRA", "SERVITEUR"]
        },
        
        "Garde royal Kree": {
            "character_id": "KreeTank_Counter",
            "visible_tags": ["SUPER-VILAIN", "COSMIQUE", "BIOTECHNIQUE", "PROTECTEUR", "KREE", "SERVITEUR"],
            "filtered_tags": ["KREE", "SERVITEUR"]
        },
        
        "Ghost Rider": {
            "character_id": "GhostRider",
            "visible_tags": ["HÉROS", "VILLE", "MYSTIQUE", "COGNEUR", "SURNATUREL", "CHASSEUR NOIR", "ESPRIT DE VENGEANCE"],
            "filtered_tags": ["SURNATUREL", "CHASSEUR NOIR", "ESPRIT DE VENGEANCE"]
        },
        
        "Ghost Rider (Robbie)": {
            "character_id": "GhostRiderRobbie",
            "visible_tags": ["HÉROS", "VILLE", "MYSTIQUE", "TIREUR", "DÉFENSEUR SECRET", "PLEIN D'ÉNERGIE", "ESPRIT DE VENGEANCE"],
            "filtered_tags": ["DÉFENSEUR SECRET", "ESPRIT DE VENGEANCE"]
        },
        
        "Ghost-Spider": {
            "character_id": "GhostSpider",
            "visible_tags": ["HÉROS", "VILLE", "BIOTECHNIQUE", "EXPERTISE", "MANIPULATEUR", "SPIDER-VERSE", "WEB WARRIOR", "SOCIÉTÉ DES ARAIGNÉES", "TISSEUR DE TOILE", "EN COUPLE"],
            "filtered_tags": ["SPIDER-VERSE", "WEB WARRIOR", "SOCIÉTÉ DES ARAIGNÉES", "TISSEUR DE TOILE"]
        },
        
        "Gladiator": {
            "character_id": "Gladiator",
            "visible_tags": ["SUPER-VILAIN", "COSMIQUE", "BIOTECHNIQUE", "PROTECTEUR", "ANNIHILATEUR"],
            "filtered_tags": ["ANNIHILATEUR"]
        },
        
        "Gorr": {
            "character_id": "Gorr",
            "visible_tags": ["SUPER-VILAIN", "COSMIQUE", "BIOTECHNIQUE", "MANIPULATEUR", "ANNIHILATEUR", "SYMBIOTE"],
            "filtered_tags": ["ANNIHILATEUR", "SYMBIOTE"]
        },
        
        "Graviton": {
            "character_id": "Graviton",
            "visible_tags": ["SUPER-VILAIN", "MONDIAL", "BIOTECHNIQUE", "MANIPULATEUR", "A.I.M."],
            "filtered_tags": ["A.I.M."]
        },
        
        "Grenadier d'Hydra": {
            "character_id": "HydraDmg_AoE",
            "visible_tags": ["SUPER-VILAIN", "MONDIAL", "TECHNO", "TIREUR", "HYDRA", "SERVITEUR"],
            "filtered_tags": ["HYDRA", "SERVITEUR"]
        },
        
        "Groot": {
            "character_id": "Groot",
            "visible_tags": ["HÉROS", "COSMIQUE", "BIOTECHNIQUE", "SOUTIEN", "GARDIEN", "FRÈRES DES ÉTOILES", "ÉLITES DE L'ANNIVERSAIRE"],
            "filtered_tags": ["GARDIEN", "FRÈRES DES ÉTOILES"]
        },
        
        "Guardian": {
            "character_id": "Guardian",
            "visible_tags": ["HÉROS", "MONDIAL", "TECHNO", "COGNEUR", "DIVISION ALPHA"],
            "filtered_tags": ["DIVISION ALPHA"]
        },
        
        "Guêpe": {
            "character_id": "Wasp",
            "visible_tags": ["HÉROS", "MONDIAL", "TECHNO", "TIREUR", "PYM TECH", "A-FORCE ABSOLUE", "EN COUPLE"],
            "filtered_tags": ["PYM TECH", "A-FORCE ABSOLUE"]
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