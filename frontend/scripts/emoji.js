let current = null;
let revealed = 1;
let allCharacters = [];
let guessedCharacters = [];

async function fetchAllCharacters() {
    try {
        const res = await fetch('/api/characters');
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

async function fetchData() {
    try {
        const res = await fetch('/emoji_random');
        current = await res.json();
        if (!current || !current.name) {
            document.getElementById('emojiBox').textContent = 'Aucun personnage trouvé.';
            return;
        }
        revealed = 1; // Affiche uniquement le premier emoji
        showEmojis();
        document.getElementById('result').textContent = '';
        document.getElementById('guessInput').value = '';
    } catch (e) {
        document.getElementById('emojiBox').textContent = 'Erreur de chargement des données.';
    }
}

function nextEmoji() {
    guessedCharacters = [];
    updateGuessedList();
    fetchData();
}

function showEmojis() {
    if (!current.emojis) {
        document.getElementById('emojiBox').textContent = 'Aucun emoji pour ce personnage.';
        return;
    }
    let emojisArr = current.emojis.split(',');
    let html = '';
    for (let i = 0; i < revealed; i++) {
        html += `<span class="emoji-char">${emojisArr[i]}</span> `;
    }
    document.getElementById('emojiBox').innerHTML = html;
}

function showVictoryAnimationEmoji() {
    const victoryDiv = document.createElement('div');
    victoryDiv.className = 'victory-animation';
    victoryDiv.id = 'victoryAnimation';
    const portraitSrc = `http://localhost:5001/portraits/Portrait_${current.character_id}.png`;
    victoryDiv.innerHTML = `
        <div class="victory-content">
            <div class="victory-title">🎉 VICTOIRE ! 🎉</div>
            <img src="${portraitSrc}" alt="${current.name}" class="victory-portrait" onerror="this.style.display='none'">
            <div class="victory-message">
                Vous avez trouvé <strong>${current.name}</strong><br>
                en ${revealed} tentative${revealed > 1 ? 's' : ''} !
            </div>
            <button class="victory-button" onclick="restartEmojiGame()">🔄 Recommencer</button>
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

function restartEmojiGame() {
    const victoryDiv = document.getElementById('victoryAnimation');
    if (victoryDiv) victoryDiv.remove();
    guessedCharacters = [];
    updateGuessedList();
    nextEmoji();
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
    // Empêche toute interaction si la victoire est affichée
    if (document.getElementById('victoryAnimation')) return;
    const guess = document.getElementById('guessInput').value.trim().toLowerCase();
    // Cherche le personnage correspondant à la saisie
    let guessedChar = allCharacters.find(char => char.alias.toLowerCase() === guess);
    if (!guessedChar && guess.length > 0) {
        // Recherche souple si pas trouvé (ex: accents, espaces)
        guessedChar = allCharacters.find(char => char.alias.toLowerCase().replace(/[^a-z0-9]/g, '') === guess.replace(/[^a-z0-9]/g, ''));
    }
    if (guess === current.name.toLowerCase()) {
        // Ajoute le personnage trouvé à la liste si pas déjà présent
        if (!guessedCharacters.some(c => c.character_id === current.character_id)) {
            guessedCharacters.push({ character_id: current.character_id, alias: current.name });
            updateGuessedList();
        }
        showVictoryAnimationEmoji();
        revealed = current.emojis.split(',').length;
        showEmojis();
        input.value = '';
        updateSearchPortrait('');
        return;
    } else {
        // Ajoute le mauvais choix à la liste si pas déjà présent et si trouvé dans la base
        if (guessedChar && !guessedCharacters.some(c => c.character_id === guessedChar.character_id)) {
            guessedCharacters.push({ character_id: guessedChar.character_id, alias: guessedChar.alias });
            updateGuessedList();
        }
        if (revealed < current.emojis.split(',').length) {
            revealed++;
            showEmojis();
            document.getElementById('result').textContent = 'Raté ! Un emoji révélé.';
        } else {
            document.getElementById('result').textContent = 'Raté !';
        }
        input.value = '';
        updateSearchPortrait('');
    }
}

// Suggestions avec portraits
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
    // Affiche tous les persos qui CONTIENNENT le terme (et plus seulement ceux qui commencent par)
    const filtered = allCharacters.filter(char => char.alias.toLowerCase().includes(searchTerm));
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

// Ajout du portrait dans la barre de recherche (comme dans Classique)
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
    fetchData();
    updateGuessedList();
};