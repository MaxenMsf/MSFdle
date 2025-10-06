# MSFdle - Marvel Strike Force Guessing Game 🎮

Un jeu de devinettes basé sur les personnages de Marvel Strike Force, inspiré de Wordle ! Devinez le personnage mystère en utilisant les indices sur l'alignement, la localisation, les origines, le rôle et les tags.

## 🎯 Comment jouer

### Modes de jeu
- **Mode Classique** : Devinez le personnage mystère Marvel Strike Force à partir d'indices colorés sur ses caractéristiques (alignement, localisation, origines, rôle, tags).
- **Mode Emoji** : Devinez le personnage mystère uniquement à partir d'une série d'emojis représentant ses caractéristiques ou son histoire !
- **Mode Capacité** : Devinez le personnage mystère uniquement à partir d'une des capacités du personnage. Une fois trouvé, il faut aussi deviner si c'est le basique, le spécial, l'ultime ou le passif du personnage !
- **Mode Pixelisé** : Devinez le personnage mystère à partir d'un portrait très pixelisé qui se dépixelise progressivement à chaque tentative !
- **Mode Hunter** : Un mini-jeu d'action où vous devez cliquer sur les héros Marvel (Iron Man) qui volent à travers l'écran avant qu'ils ne s'échappent ! La vitesse augmente progressivement pour un défi croissant.

### Règles du jeu classique
1. **Objectif** : Devinez le personnage mystère Marvel Strike Force
2. **Indices** : Chaque tentative vous donne des indices colorés :
   - 🟢 **Vert** : Correspondance exacte
   - 🟡 **Jaune** : Correspondance partielle (pour les tags/origines)
   - 🔴 **Rouge** : Aucune correspondance
3. **Catégories** : Alignement, Localisation, Origines, Rôle, Tags
4. **Portraits** : Le portrait du personnage s'affiche progressivement

### Règles du jeu Emoji
1. **Objectif** : Devinez le personnage mystère à partir d'une suite d'emojis !
2. **Indices** : À chaque mauvaise tentative, un nouvel emoji est révélé.
3. **Suggestions** : L'autocomplétion vous aide à trouver le bon personnage.
4. **Victoire** : Trouvez le personnage avec le moins de tentatives possible !

### Règles du jeu Capacité
1. Une icône de capacité est affichée (avec options de rotation et de couleur).
2. Saisissez le nom du personnage dans la barre de recherche (autocomplétion et portraits disponibles).
3. Si la réponse est correcte, choisissez le type de capacité parmi les boutons proposés.
4. Le score dépend du nombre d'essais.

### Règles du jeu Pixelisé
1. **Objectif** : Devinez le personnage mystère à partir d'un portrait très pixelisé !
2. **Indices** : À chaque mauvaise tentative, l'image se dépixelise progressivement (15 niveaux de dépixelisation).
3. **Suggestions** : L'autocomplétion avec portraits vous aide à trouver le bon personnage.
4. **Victoire** : Trouvez le personnage avec le moins de tentatives possible !

### Règles du jeu Hunter
1. **Objectif** : Cliquez sur les héros Marvel (Iron Man) qui volent à travers l'écran !
2. **Mécaniques** : 
   - Vous avez 3 vies (❤️)
   - +10 points par héros cliqué
   - Perdez une vie si un héros s'échappe de l'écran
   - La vitesse augmente toutes les 5 secondes
   - Jusqu'à 5 héros peuvent apparaître simultanément
3. **Contrôles** : Utilisez votre curseur personnalisé (gant de l'infini) pour cliquer sur les héros
4. **Ambiance** : Musique Avengers 8-bit et effet sonore du snap de Thanos à chaque clic !
5. **Victoire** : Survivez le plus longtemps possible et maximisez votre score !

### Exemple de partie classique
- Vous devinez "Spider-Man"
- Alignement : Hero ✅ (correct)
- Localisation : Ville ❌ (le personnage mystère n'est pas en Ville)
- Tags : SPIDER-VERSE 🟡 (le personnage mystère partage ce tag mais en a d'autres)

## 🚀 Installation et lancement

### Prérequis
- Python 3.7+
- Un navigateur web moderne

### 🔧 Installation
```bash
# 1. Cloner le projet
git clone https://github.com/MaxenMsf/MSFdle.git
cd MSFdle

# 2. Installer les dépendances Python
pip install flask flask-cors python-dotenv

# 3. Créer la base de données
cd backend
python rebuild_database_from_csv.py

# 4. Lancer le serveur
python app.py
```

### 🎮 Jouer
1. Ouvrez votre navigateur
2. Allez à : `http://127.0.0.1:5001`
3. Choisissez un mode de jeu et commencez à deviner !

## 📊 Fonctionnalités

### 🎯 Jeu principal
- **5 modes de jeu** : Classique (indices), Emoji (devinette par emojis), Capacité (devinette par capacité), Pixelisé (portrait pixelisé) et Hunter (mini-jeu d'action)
- **341 personnages** Marvel Strike Force
- **Système de hints intelligent** avec correspondances partielles
- **Portraits automatiques** pour chaque personnage
- **Interface responsive** et intuitive
- **Autocomplétion avancée** avec portraits dans tous les modes

### 🔧 Administration
- Interface d'admin : `http://127.0.0.1:5001/admin`
- Gestion des tags et personnages
- Statistiques du jeu

### 📱 API
- **REST API complète** pour toutes les fonctionnalités
- **Base de données SQLite** optimisée
- **Recherche avec autocomplete**
- **Système de tags normalisé**

## 📁 Structure du projet

```
MSFdle/
├── backend/
│   ├── app.py                 # Serveur Flask principal
│   ├── requirements.txt       # Dépendances Python
│   └── rebuild_database_from_csv.py  # Maintenance DB
├── frontend/
│   ├── index.html            # Menu principal
│   ├── classique_game.html   # Interface de jeu classique
│   ├── emoji_game.html       # Interface du jeu des emojis
│   ├── capacity_game.html    # Interface du jeu Capacité
│   ├── pixel_game.html       # Interface du jeu Pixelisé
│   ├── hunter_game.html      # Interface du jeu Hunter
│   ├── scripts/              # Scripts JavaScript
│   │   ├── classique.js
│   │   ├── emoji.js
│   │   ├── capacity.js
│   │   ├── pixel.js
│   │   └── hunter_game.js
│   ├── styles/               # Feuilles de style CSS
│   │   ├── style.css
│   │   ├── emoji.css
│   │   ├── capacity.css
│   │   ├── pixel.css
│   │   └── hunter_game.css
│   ├── portraits/            # Images des personnages (339 portraits)
│   └── hunter/               # Ressources du mode Hunter
│       ├── sprites/          # Sprites animés (Iron Man, curseur)
│       ├── music/            # Musique et effets sonores
│       └── hunter_background.png
├── data/
│   ├── perso.csv             # Données des personnages
│   └── msfdle.db             # Base de données SQLite
├── database/
│   └── schema.sql            # Structure de la base
└── README.md                 # Ce fichier
```

## 🗄️ Base de données

### Structure optimisée
- **Table `characters`** : Informations principales des personnages
- **Table `tags`** : Tags normalisés et réutilisables  
- **Table `character_tags`** : Relations many-to-many
- **Index optimisés** pour de meilleures performances

### Données
- **341 personnages** avec toutes leurs caractéristiques
- **Tags intégrés** depuis le CSV (équipes, affiliations, etc.)
- **Portraits automatiquement liés** via character_id

## 🎮 API Endpoints

### Jeu
- `GET /` - Interface principale (menu)
- `GET /api/random-character` - Personnage mystère (mode classique)
- `GET /emoji_random` - Personnage mystère avec emojis (mode emoji)
- `POST /api/guess` - Vérifier une tentative
- `GET /api/search?q=spider` - Recherche avec autocomplete
- `GET /api/characters` - Liste tous les personnages

## 🔧 Maintenance

### Ajouter de nouveaux personnages
1. Modifiez le fichier `data/perso.csv`
2. Ajoutez le portrait dans `frontend/portraits/Portrait_{CharacterId}.png`
3. Exécutez : `python backend/rebuild_database_from_csv.py`

### Format CSV
```csv
Character Id,Alias,Alignement,Localisation,Origine,Origine2,Unique,Role,Tags,emojis
SpiderMan,Spider-Man,Hero,Ville,Biotechnique,,Formule,Cogneur,"SPIDER-VERSE,WEB WARRIOR","🕷️,🕸️,🦸‍♂️"
```

## 🎨 Personnalisation

### Modifier l'interface
- Éditez les fichiers HTML dans `frontend/`
- Les styles CSS sont dans le dossier `frontend/styles/`
- Les scripts JavaScript sont dans `frontend/scripts/`

### Ajouter des fonctionnalités
- Modifiez `backend/app.py` pour l'API
- La base de données est extensible

## 🔄 Arrêter le serveur

- Appuyez sur `Ctrl+C` dans le terminal
- Ou fermez la fenêtre du terminal

## 📝 Développement

Ce projet utilise :
- **Backend** : Flask (Python)
- **Frontend** : HTML/CSS/JavaScript vanilla
- **Base de données** : SQLite
- **API** : REST avec JSON

---

## 🎉 Amusez-vous bien !

Développé avec ❤️ pour les fans de Marvel Strike Force