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

# Tags des personnages extraits des captures d'écran
character_tags = {
    "Swarm": ["SPIDER-VERSE", "SINISTER SIX", "INFESTATION"],
    "HandTank_Stealth": ["MAIN"],
    "Falcon": ["TECHNO-ARMURE", "MIGHTY AVENGERS", "UNCANNY AVENGERS"],
    "FalconJoaquin": ["LIBERTÉ"],
    "ShieldDmg_Defense": ["S.H.I.E.L.D"],
    "Ghost": ["PYM TECH", "THUNDERBOLT"],
    "Fantomex": ["UNLIMITED X-MEN"],
    "KreeDmg_Speed": ["KREE"],
    "Beast": ["UNCANNY X-MEN", "ASTONISHING X-MEN", "IMMORTAL X-MEN", "UNCANNY AVENGERS"],
    "DarkBeast": ["GRAINE DE MORT"],
    "InvisibleWoman": ["QUATRE FANTASTIQUES", "MIGHTY AVENGERS"],
    "InvisibleWomanMCU": ["QUATRE FANTASTIQUES (MCU)"],
    "Sunfire": ["UNLIMITED X-MEN", "DIVISION ALPHA"],
    "Firestar": ["NEW WARRIOR"],
    "Forge": ["X-TREME X-MEN"],
    "FranklinRichards": ["QUATRE FANTASTIQUES (MCU)"],
    "HydraDmg_Buff": ["HYDRA"],
    "Gambit": ["UNLIMITED X-MEN", "X-TREME X-MEN"],
    "Gamora": ["GARDIEN", "INFINITY WATCH"],
    "HydraTank_Taunt": ["HYDRA"],
    "KreeTank_Counter": ["KREE"],
    "GhostRider": ["SURNATUREL", "CHASSEUR NOIR", "ESPRIT DE VENGEANCE"],
    "GhostRiderRobbie": ["DÉFENSEUR SECRET", "ESPRIT DE VENGEANCE"],
    "GhostSpider": ["SPIDER-VERSE", "WEB WARRIOR", "SOCIÉTÉ DES ARAIGNÉES"],
    "Gladiator": ["ANNIHILATEUR"],
    "Gorr": ["ANNIHILATEUR", "SYMBIOTE"],
    "Graviton": ["A.I.M."],
    "HydraDmg_AoE": ["HYDRA"],
    "Groot": ["GARDIEN", "FRÈRES DES ÉTOILES"],
    "Guardian": ["DIVISION ALPHA"],
    "Wasp": ["PYM TECH", "A-FORCE ABSOLUE"],
}

# Tags disponibles (sera rempli automatiquement)
available_tags = [
    "A-FORCE ABSOLUE",
    "A.I.M.",
    "ANNIHILATEUR",
    "ASTONISHING X-MEN",
    "CHASSEUR NOIR",
    "DIVISION ALPHA",
    "DÉFENSEUR SECRET",
    "ESPRIT DE VENGEANCE",
    "FRÈRES DES ÉTOILES",
    "GARDIEN",
    "GRAINE DE MORT",
    "HYDRA",
    "IMMORTAL X-MEN",
    "INFESTATION",
    "INFINITY WATCH",
    "KREE",
    "LIBERTÉ",
    "MAIN",
    "MIGHTY AVENGERS",
    "NEW WARRIOR",
    "PYM TECH",
    "QUATRE FANTASTIQUES",
    "QUATRE FANTASTIQUES (MCU)",
    "S.H.I.E.L.D",
    "SINISTER SIX",
    "SOCIÉTÉ DES ARAIGNÉES",
    "SPIDER-VERSE",
    "SURNATUREL",
    "SYMBIOTE",
    "TECHNO-ARMURE",
    "THUNDERBOLT",
    "UNCANNY AVENGERS",
    "UNCANNY X-MEN",
    "UNLIMITED X-MEN",
    "WEB WARRIOR",
    "X-TREME X-MEN",
]