# MSFdle - Marvel Strike Force Guessing Game 🎮

Un jeu de devinettes basé sur les personnages de Marvel Strike Force, inspiré de Wordle ! Devinez le personnage mystère en utilisant les indices sur l'alignement, la localisation, les origines, le rôle et les tags.

## 🎯 Comment jouer

### Règles du jeu
1. **Objectif** : Devinez le personnage mystère Marvel Strike Force
2. **Indices** : Chaque tentative vous donne des indices colorés :
   - 🟢 **Vert** : Correspondance exacte
   - 🟡 **Jaune** : Correspondance partielle (pour les tags/origines)
   - 🔴 **Rouge** : Aucune correspondance
3. **Catégories** : Alignement, Localisation, Origines, Rôle, Tags
4. **Portraits** : Le portrait du personnage s'affiche progressivement

### Exemple de partie
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

# 4. Créer la base de données
cd backend
python rebuild_database_from_csv.py

# 4. Lancer le serveur
python app.py
```

### 🎮 Jouer
1. Ouvrez votre navigateur
2. Allez à : `http://127.0.0.1:5001`
3. Commencez à deviner !

## 📊 Fonctionnalités

### 🎯 Jeu principal
- **338 personnages** Marvel Strike Force
- **91 tags uniques** (équipes, affiliations, etc.)
- **Système de hints intelligent** avec correspondances partielles
- **Portraits automatiques** pour chaque personnage
- **Interface responsive** et intuitive

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
│   ├── test_game_clean.html   # Interface de jeu
│   ├── admin_tags.html        # Interface d'admin
│   └── portraits/             # Images des personnages (339 portraits)
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
- **338 personnages** avec toutes leurs caractéristiques
- **Tags intégrés** depuis le CSV (équipes, affiliations, etc.)
- **Portraits automatiquement liés** via character_id

## 🎮 API Endpoints

### Jeu
- `GET /` - Interface de jeu
- `GET /api/random-character` - Personnage mystère
- `POST /api/guess` - Vérifier une tentative
- `GET /api/search?q=spider` - Recherche avec autocomplete

### Administration
- `GET /admin` - Interface d'administration
- `GET /api/characters` - Liste tous les personnages
- `GET /api/tags` - Liste tous les tags
- `POST /api/characters` - Créer un personnage
- `PUT /api/characters/{id}` - Modifier un personnage

### Système
- `GET /api/health` - État de l'API
- `GET /api/test-db` - Test de la base de données

## 🔧 Maintenance

### Ajouter de nouveaux personnages
1. Modifiez le fichier `data/perso.csv`
2. Ajoutez le portrait dans `frontend/portraits/Portrait_{CharacterId}.png`
3. Exécutez : `python backend/rebuild_database_from_csv.py`

### Format CSV
```csv
Character Id,Alias,Alignement,Localisation,Origine,Origine2,Unique,Role,Tags
SpiderMan,Spider-Man,Hero,Ville,Biotechnique,,Formule,Cogneur,"SPIDER-VERSE,WEB WARRIOR"
```

## 🎨 Personnalisation

### Modifier l'interface
- Éditez `frontend/test_game_clean.html`
- Les styles CSS sont intégrés dans le fichier

### Ajouter des fonctionnalités
- Modifiez `backend/app.py` pour l'API
- La base de données est extensible

## 🏆 Statistiques

- **338 personnages** disponibles
- **91 tags uniques** (SPIDER-VERSE, X-MEN, AVENGER, etc.)
- **556 associations** personnage-tag
- **339 portraits** haute qualité

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
├── database/           # Schéma SQL
│   └── schema.sql
├── scripts/            # Scripts d'import
│   └── import_data.py
└── data/              # Données CSV
    └── perso.csv
```

## 🚀 Plan de développement

### Phase 1: Backend API (Flask)
1. **Setup Flask avec PostgreSQL**
2. **Routes API essentielles:**
   - `GET /api/random-character` - Personnage à deviner
   - `GET /api/characters` - Liste tous les personnages
   - `POST /api/guess` - Vérifier une proposition
   - `GET /api/character/{id}` - Détails d'un personnage

### Phase 2: Frontend (React)
1. **Interface de jeu:**
   - Zone de saisie avec autocomplete
   - Grille des tentatives avec code couleur
   - Système de victoire/défaite
2. **Logique de comparaison:**
   - Vert: correspondance exacte
   - Jaune: correspondance partielle (pour les origines)
   - Rouge: aucune correspondance

### Phase 3: Déploiement
1. **Base de données:** Supabase (PostgreSQL gratuit)
2. **Backend:** Railway (Flask gratuit)
3. **Frontend:** Vercel (React gratuit)

## 🎨 Interface utilisateur

Inspiré de Loldle avec:
- Header avec logo MSFdle
- Zone de recherche avec autocomplete
- Tableau des tentatives avec indicateurs colorés
- Statistiques de jeu
- Bouton "Nouveau jeu"

## 🎲 Logique de jeu

Chaque personnage est comparé sur:
- **Affiliation:** Hero/Vilain (Vert/Rouge)
- **Localisation:** Ville/Mondial/Cosmique (Vert/Rouge)
- **Origine 1:** Match exact (Vert/Rouge)
- **Origine 2:** Partielle si une des deux correspond (Jaune/Rouge)
- **Rôle:** Support/Cogneur/etc. (Vert/Rouge)
- **Tags:** À implémenter plus tard

## 📦 Technologies utilisées

- **Frontend:** React + Vite + TypeScript + Tailwind CSS
- **Backend:** Flask + SQLAlchemy + PostgreSQL
- **Base de données:** PostgreSQL (Supabase)
- **Déploiement:** Vercel + Railway + Supabase
