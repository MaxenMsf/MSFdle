// Variables globales pour le mode Pixelisé
let current = null;
let attempts = 0;
let allCharacters = [];
let guessedCharacters = [];
let currentCharacterId = null;
let originalImage = null;
let canvas = null;
let ctx = null;

// Niveaux de pixelisation (commencer très pixelisé et dépixeliser progressivement)
// Plus d'étapes pour une progression plus lente
const PIXEL_LEVELS = [80, 64, 48, 36, 28, 22, 18, 14, 12, 10, 8, 6, 4, 3, 2]; // 100 = très pixelisé, 2 = image nette

async function fetchAllCharacters() {
    try {
        const res = await fetch('http://localhost:5001/api/characters');
        const data = await res.json();
        if (data.success) {
            allCharacters = data.characters;
        } else {
            allCharacters = [];
        }
    } catch (e) {
        allCharacters = [];
    }
}

async function fetchRandomCharacter() {
    try {
        // Récupérer un personnage aléatoire depuis allCharacters
        if (allCharacters.length === 0) {
            document.getElementById('result').textContent = 'Aucun personnage disponible.';
            return;
        }
        
        const randomIndex = Math.floor(Math.random() * allCharacters.length);
        current = allCharacters[randomIndex];
        currentCharacterId = current.character_id;
        
        attempts = 0;
        updateAttemptsCounter();
        loadCharacterPortrait();
        document.getElementById('result').textContent = '';
        document.getElementById('guessInput').value = '';
        
    } catch (e) {
        document.getElementById('result').textContent = 'Erreur de chargement des données.';
    }
}

function loadCharacterPortrait() {
    if (!current || !currentCharacterId) return;
    
    const img = new Image();
    img.crossOrigin = 'anonymous';
    
    img.onload = function() {
        originalImage = img;
        drawPixelatedImage(PIXEL_LEVELS[0]); // Commencer avec 100 (très pixelisé)
    };
    
    img.onerror = function() {
        // Si le portrait n'existe pas, utiliser une image par défaut
        ctx.fillStyle = '#2a2f4a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ffffff';
        ctx.font = '16px Inter';
        ctx.textAlign = 'center';
        ctx.fillText('Portrait non disponible', canvas.width/2, canvas.height/2);
    };
    
    img.src = `http://localhost:5001/portraits/Portrait_${currentCharacterId}.png`;
}

function drawPixelatedImage(pixelSize) {
    if (!originalImage || !ctx) return;
    
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;
    
    // Effacer le canvas
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    
    if (pixelSize <= 2) {
        // Image normale (nette)
        ctx.drawImage(originalImage, 0, 0, canvasWidth, canvasHeight);
        return;
    }
    
    // Créer un canvas temporaire pour la pixelisation
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    
    // Calculer les dimensions pixelisées (TRÈS petites au début)
    const pixelWidth = Math.max(1, Math.floor(canvasWidth / pixelSize));
    const pixelHeight = Math.max(1, Math.floor(canvasHeight / pixelSize));
    
    tempCanvas.width = pixelWidth;
    tempCanvas.height = pixelHeight;
    
    // Dessiner l'image en très petit (effet pixelisé extrême)
    tempCtx.drawImage(originalImage, 0, 0, pixelWidth, pixelHeight);
    
    // Désactiver le lissage pour un effet pixelisé net
    ctx.imageSmoothingEnabled = false;
    
    // Redessiner en grand pour créer l'effet pixelisé
    ctx.drawImage(tempCanvas, 0, 0, pixelWidth, pixelHeight, 0, 0, canvasWidth, canvasHeight);
}

function updateAttemptsCounter() {
    document.getElementById('attemptsCounter').textContent = `Tentatives: ${attempts}`;
}

function nextPixelGame() {
    guessedCharacters = [];
    updateGuessedList();
    fetchRandomCharacter();
}

function showVictoryAnimationPixel() {
    const victoryDiv = document.createElement('div');
    victoryDiv.className = 'victory-animation';
    victoryDiv.id = 'victoryAnimation';
    const portraitSrc = `http://localhost:5001/portraits/Portrait_${currentCharacterId}.png`;
    
    victoryDiv.innerHTML = `
        <div class="victory-content">
            <div class="victory-title">🎉 VICTOIRE ! 🎉</div>
            <img src="${portraitSrc}" alt="${current.alias}" class="victory-portrait" onerror="this.style.display='none'">
            <div class="victory-message">
                Vous avez trouvé <strong>${current.alias}</strong><br>
                en ${attempts} tentative${attempts > 1 ? 's' : ''} !
            </div>
            <button class="victory-button" onclick="restartPixelGame()">🔄 Recommencer</button>
        </div>
    `;

    // Confettis
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'victory-confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.animationDelay = Math.random() * 3 + 's';
        confetti.style.backgroundColor = ['#FCD34D', '#10B981', '#F59E0B', '#3B82F6'][Math.floor(Math.random() * 4)];
        victoryDiv.appendChild(confetti);
    }

    document.body.appendChild(victoryDiv);
}

function restartPixelGame() {
    const victoryDiv = document.getElementById('victoryAnimation');
    if (victoryDiv) victoryDiv.remove();
    guessedCharacters = [];
    updateGuessedList();
    nextPixelGame();
}

function updateGuessedList() {
    const guessedListDiv = document.getElementById('guessedList');
    if (!guessedListDiv) return;
    if (guessedCharacters.length === 0) {
        guessedListDiv.innerHTML = '';
        return;
    }
    guessedListDiv.innerHTML = guessedCharacters.map(char => {
        const portrait = `http://localhost:5001/portraits/Portrait_${char.character_id}.png`;
        return `<div style="display:inline-flex;align-items:center;margin:0 12px 12px 0;padding:6px 12px;background:#181c2f;border-radius:12px;box-shadow:0 2px 8px #0003;">
            <img src="${portrait}" alt="${char.alias}" style="width:32px;height:32px;object-fit:cover;border-radius:50%;margin-right:10px;box-shadow:0 2px 8px #0006;">
            <span style="color:#fff;font-weight:500;">${char.alias}</span>
        </div>`;
    }).join('');
}

function submitGuess() {
    if (document.getElementById('victoryAnimation')) return;
    const guess = document.getElementById('guessInput').value.trim().toLowerCase();
    
    // Si le champ est vide, ne rien faire
    if (guess.length === 0) {
        return;
    }
    
    attempts++;
    updateAttemptsCounter();
    
    let guessedChar = allCharacters.find(char => char.alias.toLowerCase() === guess);
    if (!guessedChar && guess.length > 0) {
        guessedChar = allCharacters.find(char => char.alias.toLowerCase().replace(/[^a-z0-9]/g, '') === guess.replace(/[^a-z0-9]/g, ''));
    }
    
    if (guess === current.alias.toLowerCase()) {
        // Bonne réponse
        if (!guessedCharacters.some(c => c.character_id === currentCharacterId)) {
            guessedCharacters.push({ character_id: currentCharacterId, alias: current.alias });
            updateGuessedList();
        }
        showVictoryAnimationPixel();
        // Afficher l'image complète (nette)
        drawPixelatedImage(2);
        input.value = '';
        updateSearchPortrait('');
        return;
    } else {
        // Mauvaise réponse - ajouter à la liste des tentatives
        if (guessedChar && !guessedCharacters.some(c => c.character_id === guessedChar.character_id)) {
            guessedCharacters.push({ character_id: guessedChar.character_id, alias: guessedChar.alias });
            updateGuessedList();
        }
        
        // Dépixeliser progressivement (passer au niveau suivant)
        const levelIndex = Math.min(attempts, PIXEL_LEVELS.length - 1);
        drawPixelatedImage(PIXEL_LEVELS[levelIndex]);
        
        if (attempts >= PIXEL_LEVELS.length - 1) {
            document.getElementById('result').textContent = 'Image complètement révélée !';
        } else {
            document.getElementById('result').textContent = 'Raté ! Image un peu moins pixelisée.';
        }
        
        input.value = '';
        updateSearchPortrait('');
    }
}

// Suggestions avec portraits (même logique que les autres modes)
const input = document.getElementById('guessInput');
const suggestions = document.getElementById('suggestions');

input.addEventListener('input', (e) => {
    const value = e.target.value.trim();
    showSuggestions(value);
});

input.addEventListener('focus', (e) => {
    showSuggestions(e.target.value.trim());
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.input-row')) {
        suggestions.style.display = 'none';
    }
});

function showSuggestions(value) {
    if (!allCharacters.length || value.length < 1) {
        suggestions.style.display = 'none';
        return;
    }
    const searchTerm = value.toLowerCase();
    // Exclure les persos déjà devinés ou proposés
    const excludedIds = guessedCharacters.map(c => c.character_id);
    const filtered = allCharacters.filter(char => char.alias.toLowerCase().includes(searchTerm) && !excludedIds.includes(char.character_id));
    if (filtered.length === 0) {
        suggestions.style.display = 'none';
        return;
    }
    suggestions.innerHTML = filtered.map(char => {
        let portraitName = `http://localhost:5001/portraits/Portrait_${char.character_id}.png`;
        return `<div class="suggestion" style="display:flex;align-items:center;padding:12px 20px;cursor:pointer;transition:all 0.3s;background:#181c2f;border-bottom:1px solid #3b82f6;" onclick="selectCharacter('${char.alias.replace(/'/g, "\\'")}')"><img src="${portraitName}" alt="portrait" style="width:32px;height:32px;object-fit:cover;border-radius:50%;margin-right:14px;box-shadow:0 2px 8px #0006;"><span>${char.alias}</span></div>`;
    }).join('');
    suggestions.style.display = 'block';
}

function selectCharacter(name) {
    input.value = name;
    suggestions.style.display = 'none';
    input.focus();
    submitGuess();
}

// Ajout du portrait dans la barre de recherche
const searchPortrait = document.createElement('img');
searchPortrait.id = 'searchPortrait';
searchPortrait.className = 'search-portrait';
searchPortrait.style.display = 'none';
searchPortrait.style.position = 'absolute';
searchPortrait.style.left = '16px';
searchPortrait.style.top = '50%';
searchPortrait.style.transform = 'translateY(-50%)';
searchPortrait.style.width = '36px';
searchPortrait.style.height = '36px';
searchPortrait.style.borderRadius = '50%';
searchPortrait.style.objectFit = 'cover';
searchPortrait.style.boxShadow = '0 2px 8px #0006';

// Insérer le portrait dans le DOM
window.addEventListener('DOMContentLoaded', () => {
    const inputRow = document.querySelector('.input-row > div');
    if (inputRow) {
        inputRow.insertBefore(searchPortrait, inputRow.firstChild);
    }
    
    // Initialiser le canvas
    canvas = document.getElementById('pixelCanvas');
    ctx = canvas.getContext('2d');
});

function updateSearchPortrait(value) {
    if (value.length < 1) {
        searchPortrait.style.display = 'none';
        return;
    }
    let match = allCharacters.find(char =>
        char.alias.toLowerCase() === value.toLowerCase()
    );
    if (match) {
        const portraitSrc = `http://localhost:5001/portraits/Portrait_${match.character_id}.png`;
        searchPortrait.src = portraitSrc;
        searchPortrait.style.display = 'block';
        searchPortrait.onerror = () => {
            searchPortrait.style.display = 'none';
        };
    } else {
        searchPortrait.style.display = 'none';
    }
}

// Mettre à jour le portrait à chaque saisie
input.addEventListener('input', (e) => {
    const value = e.target.value.trim();
    showSuggestions(value);
    updateSearchPortrait(value);
});

input.addEventListener('focus', (e) => {
    showSuggestions(e.target.value.trim());
    updateSearchPortrait(e.target.value.trim());
});

window.onload = async function () {
    await fetchAllCharacters();
    
    // Initialiser le canvas
    canvas = document.getElementById('pixelCanvas');
    ctx = canvas.getContext('2d');
    
    fetchRandomCharacter();
    updateGuessedList();
};
