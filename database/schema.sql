-- Schema optimisé pour MSFdle
-- Exclusion de Character ID et Unique comme demandé

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    alias VARCHAR(200) UNIQUE NOT NULL,
    alignment VARCHAR(20) NOT NULL, -- Hero/Vilain
    location VARCHAR(50) NOT NULL, -- Ville/Mondial/Cosmique
    origin1 VARCHAR(50) NOT NULL, -- Première origine obligatoire
    origin2 VARCHAR(50), -- Deuxième origine (optionnel)
    role VARCHAR(50) NOT NULL -- Support/Cogneur/Manipulateur/Protecteur/Tireur
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE character_tags (
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (character_id, tag_id)
);

-- Index pour optimiser les recherches du jeu
CREATE INDEX idx_characters_alignment ON characters(alignment);
CREATE INDEX idx_characters_location ON characters(location);
CREATE INDEX idx_characters_origin1 ON characters(origin1);
CREATE INDEX idx_characters_origin2 ON characters(origin2);
CREATE INDEX idx_characters_role ON characters(role);
CREATE INDEX idx_character_tags_character ON character_tags(character_id);

-- Table pour les parties (pour futures statistiques)
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    target_character_id INTEGER REFERENCES characters(id),
    attempts INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vue pratique pour récupérer un personnage avec ses tags
CREATE VIEW character_with_tags AS
SELECT 
    c.*,
    COALESCE(
        STRING_AGG(t.name, ', ' ORDER BY t.name), 
        ''
    ) as tags
FROM characters c
LEFT JOIN character_tags ct ON c.id = ct.character_id
LEFT JOIN tags t ON ct.tag_id = t.id
GROUP BY c.id, c.alias, c.alignment, c.location, c.origin1, c.origin2, c.role;
