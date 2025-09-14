#!/usr/bin/env python3
"""
Tags extraits des nouvelles captures d'écran MSF
"""

# Tags à ignorer (non pertinents pour le jeu)
IGNORED_TAGS = [
    "LEGENDARY", "ELITE DE L'ANNIVERSAIRE", "ELITES DE L'ANNIVERSAIRE",
    "HORS DU TEMPS", "RENAISSANCE", "UNI", "EN COUPLE", "ETERNEL",
    "JUNETEENTH", "A-FORCE", "CONFRERIE", "UNCANNY X-MEN", "DEADPOOL ET SES COPAINS",
    "KREE", "MILITAIRE", "COGNEUR", "SOUTIEN", "TIREUR", "PROTECTEUR", "MANIPULATEUR",
    "RAVAGEUR", "SERVITEUR", "GARDIEN", "MILLE-PART", "NEW WARRIOR",
    "AVENGERS SECRETS", "LIBERTE", "ENVAHISSEUR", "X-FORCE", "IMMORTAL X-MEN",
    "AVENGER - VAGUE1", "HEROS A LOUER", "DEFENSEUR SECRET", "A.I.M.", "SERVITEUR",
    "FILS DE LOKI"
]

# Nouveaux personnages avec leurs tags extraits
character_tags = {
    "Bouffon Vert": ["SPIDER-VERSE", "SINISTER SIX", "PERE"],
    "Bouffon Vert (Classique)": ["SPIDER-VERSE", "SINISTER SIX", "SUPERIOR SIX", "ENNEMI JURE"],
    "Brawn": ["GAMMA"],
    "Bucky Barnes": ["INVAHISSEUR"],  # Tag visible dans l'image
    "Bullseye": ["MERCENAIRE"],
    "Cable": ["HORS DU TEMPS", "ESPRIT DE VENGEANCE"],  # Tags visibles
    "Cape": ["NEW WARRIOR"],
    "Captain America": ["S.H.I.E.L.D", "MILITAIRE", "AVENGER - VAGUE1", "HORS DU TEMPS"],
    "Captain America (2GM)": ["ENVAHISSEUR"],
    "Captain America (Sam)": ["AVENGERS SECRETS", "LIBERTE"],
    "Captain Britain": ["ILLUMINATI", "EPIQUE"],
    "Captain Carter": ["RENAISSANCE", "HORS DU TEMPS"],
    "Captain Marvel": ["KREE", "MILITAIRE", "A-FORCE"],
    "Carnage": ["SPIDER-VERSE", "SYMBIOTE", "CONSCIENCE COLLECTIVE"],
    "Chatte Noire": ["SPIDER-VERSE", "DEFENSEUR SECRET"],
    "Chercheuse de l'A.I.M": ["A.I.M", "SERVITEUR"],
    "Chevalier Noir": ["HORS DU TEMPS"],
    "Circe": ["ETERNEL"],
    "Cogneur Ravageur": ["RAVAGEUR", "SERVITEUR"],
    "Colleen Wing": ["HEROS A LOUER"],
    "Colosse": ["CONFRERIE"],
    "Colossus": ["UNCANNY X-MEN", "DEADPOOL ET SES COPAINS"],
    "Corvus Glaive": ["ORDRE NOIR"],
    "Cosmic Ghost Rider": ["HORS DU TEMPS", "ESPRIT DE VENGEANCE"],
    "Cosmo": ["GARDIEN", "MILLE-PART"],
    "Crâne Rouge": ["HYDRA", "ENNEMI JURE"]
}

print("📋 Tags extraits des captures d'écran:")
for character, tags in character_tags.items():
    filtered_tags = [tag for tag in tags if tag not in IGNORED_TAGS]
    if filtered_tags:
        print(f"  {character}: {', '.join(filtered_tags)}")
    else:
        print(f"  {character}: AUCUN")