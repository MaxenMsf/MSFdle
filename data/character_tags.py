# Tags extraits depuis les captures d'écran MSF
# Format: character_id = ["tag1", "tag2", "tag3"]

# Tags à IGNORER (ne pas extraire des captures d'écran)
IGNORED_TAGS = [
    # Tags déjà existants dans le jeu (colonnes principales)
    "Hero", "Vilain", "Ville", "Mondial", "Cosmique", "Mystique", "Techno", 
    "Expertise", "Mutant", "Biotechnique", "Tireur", "Cogneur", "Protecteur", 
    "Manipulateur", "Soutien",
    
    # Variantes en français  
    "HÉROS", "SUPER-VILAIN", "VILLE", "MONDIAL", "COSMIQUE", "MYSTIQUE", "TECHNO",
    "EXPERTISE", "MUTANT", "BIOTECHNIQUE", "TIREUR", "COGNEUR", "PROTECTEUR",
    "MANIPULATEUR", "SOUTIEN",
    
    # Tags à ignorer spécifiquement
    "Atout du S.T.R.I.K.E", "Chapitre 1 - Annonciateur", "Chapitre 2 - Conquerant", 
    "Deadpool et ses copains", "élites de l'anniversaire", "en couple", "ennemi juré", 
    "épique", "esprit de vengance", "exposé", "juneteenth", "le casse de nulle-part", 
    "légendaire", "mères marvel", "msf original", "mythique", "plein d'énergie", 
    "serviteur", "tisseur de toile", "uni",
    
    # Variantes en majuscules
    "CHAPITRE 2 - CONQUÉRANT", "DEADPOOL ET SES COPAINS", "PLEIN D'ÉNERGIE", "LÉGENDAIRE"
]

# Tags des personnages (vide pour l'instant)
character_tags = {
    "PhantomRider": ["SECRET WARRIOR"],
    "Scorpion": ["SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX", "INFESTATION"],
    "SuperiorSpiderMan": ["SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX", "SUPERIOR SIX"],
    "Hobgoblin": ["SPIDER-VERSE", "SINISTER SIX", "INSIDIOUS SIX"],
    "Domino": ["X-FORCE", "SECRET WARRIOR"],
    "Negasonic": ["X-FORCE", "SECRET WARRIOR"],
    "Quake": ["S.H.I.E.L.D", "INHUMAN", "SECRET WARRIOR"],
    "Shocker": ["SPIDER-VERSE", "SINISTER SIX"],
    "Vulture": ["SPIDER-VERSE", "SINISTER SIX"],
    "YoYo": ["S.H.I.E.L.D", "INHUMAN", "SECRET WARRIOR"],
    "Abomination": ["GAMMA"],
    "AdamWarlock": ["INFINITY WATCH"],
}

# Tags disponibles (sera rempli automatiquement)
available_tags = [
    "GAMMA",
    "INFESTATION",
    "INFINITY WATCH",
    "INHUMAN",
    "INSIDIOUS SIX",
    "S.H.I.E.L.D",
    "SECRET WARRIOR",
    "SINISTER SIX",
    "SPIDER-VERSE",
    "SUPERIOR SIX",
    "X-FORCE",
]