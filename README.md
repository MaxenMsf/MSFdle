# MSFdle - Marvel Strike Force Guessing Game

## 🎯 Architecture du projet

```
MSFdle/
├── frontend/           # React app (Vite)
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── backend/            # Flask API
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   └── utils/
│   ├── requirements.txt
│   └── app.py
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