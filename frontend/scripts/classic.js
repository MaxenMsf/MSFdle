let allCharacters = [];
let targetCharacter = null;
let guessHistory = [];
let gameWon = false;

const input = document.getElementById('characterInput');
const suggestions = document.getElementById('suggestions');
const messageDiv = document.getElementById('message');
const historyDiv = document.getElementById('guessHistory');
const attemptCountDiv = document.getElementById('attemptCount');
const searchPortrait = document.getElementById('searchPortrait');

// Charger tous les personnages au démarrage
async function loadCharacters() {
    try {
        const response = await fetch('http://localhost:5001/api/characters');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.success) {
            allCharacters = data.characters;

            if (allCharacters.length === 0) {
                throw new Error('Aucun personnage trouvé dans la base de données');
            }
        } else {
            throw new Error(data.error || 'Erreur lors du chargement des personnages');
        }

    } catch (error) {
        console.error('❌ Erreur chargement personnages:', error);
        showMessage('❌ Erreur de chargement des personnages: ' + error.message, 'error');
    }
}

// Événements d'entrée
input.addEventListener('input', (e) => {
    const value = e.target.value.trim();
    showSuggestions(value);
    updateSearchPortrait(value);
});

input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        makeGuess();
    }
});

// Cacher les suggestions quand on clique ailleurs
document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) {
        suggestions.style.display = 'none';
    }
});

// Afficher/masquer le loading
function showLoading(show) {
    if (show) {
        messageDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Recherche en cours...</div>';
        messageDiv.className = 'message info';
        messageDiv.style.display = 'block';
    } else {
        messageDiv.style.display = 'none';
    }
}

// Commencer une nouvelle partie
async function startNewGame() {
    showLoading(true);

    try {
        const response = await fetch('http://localhost:5001/api/random-character', {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.id) {
            targetCharacter = data;
            guessHistory = [];
            gameWon = false;
            input.disabled = false;
            input.value = '';
            messageDiv.style.display = 'none';
            historyDiv.innerHTML = '';
            attemptCountDiv.textContent = '0';

            showMessage('🎯 Nouvelle partie commencée ! Devinez le personnage...', 'info');
        } else {
            throw new Error('Réponse API invalide - pas d\'ID trouvé');
        }
    } catch (error) {
        showMessage('❌ Erreur lors du démarrage de la partie: ' + error.message, 'error');
        console.error('Erreur startNewGame:', error);
    } finally {
        showLoading(false);
    }
}

// Filtrer et afficher les suggestions
function showSuggestions(value) {
    if (value.length < 1) {
        suggestions.style.display = 'none';
        return;
    }
    const searchTerm = value.toLowerCase().trim();
    // Exclure les persos déjà devinés ou proposés
    const excludedIds = guessHistory.map(g => g.character.character_id);
    const filtered = allCharacters.filter(char => {
        const alias = char.alias.toLowerCase();
        return alias.startsWith(searchTerm) && !excludedIds.includes(char.character_id);
    });
    if (filtered.length === 0) {
        suggestions.style.display = 'none';
        return;
    }
    suggestions.innerHTML = filtered.map(char => {
        const portraitSrc = `http://localhost:5001/portraits/Portrait_${char.character_id}.png`;
        return `
            <div class="suggestion" onclick="selectCharacter('${char.alias}')">
                <img src="${portraitSrc}" alt="${char.alias}" class="suggestion-portrait" onerror="this.style.display='none'">
                <span>${char.alias}</span>
            </div>
        `;
    }).join('');
    suggestions.style.display = 'block';
}

// Sélectionner un personnage depuis les suggestions
function selectCharacter(name) {
    input.value = name;
    suggestions.style.display = 'none';
    updateSearchPortrait(name);
    makeGuess();
}

// Mettre à jour le portrait dans la barre de recherche
function updateSearchPortrait(value) {
    if (value.length < 1) {
        searchPortrait.style.display = 'none';
        return;
    }

    // Recherche exact
    let match = allCharacters.find(char =>
        char.alias.toLowerCase() === value.toLowerCase()
    );

    if (match) {
        // Utiliser le character_id pour construire le chemin du portrait
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

// Faire une tentative
async function makeGuess() {
    const characterName = input.value.trim();
    if (!characterName || gameWon) return;

    // Recherche exacte d'abord
    let guessedCharacter = allCharacters.find(char =>
        char.alias.toLowerCase() === characterName.toLowerCase()
    );

    // Si pas trouvé, recherche souple
    if (!guessedCharacter) {
        const searchTerm = characterName.toLowerCase().replace(/[^a-z0-9]/g, '');
        guessedCharacter = allCharacters.find(char => {
            const alias = char.alias.toLowerCase().replace(/[^a-z0-9]/g, '');
            return alias === searchTerm;
        });
    }

    if (!guessedCharacter) {
        showMessage('❌ Personnage non trouvé. Vérifiez l\'orthographe ou utilisez les suggestions.', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('http://localhost:5001/api/guess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                character_name: guessedCharacter.alias,
                target_id: targetCharacter.id
            })
        });

        const result = await response.json();

        // Ajouter à l'historique
        guessHistory.push({
            character: guessedCharacter,
            comparison: result.comparison || {
                alignment: guessedCharacter.alignment === targetCharacter.alignment ? 'correct' : 'incorrect',
                location: guessedCharacter.location === targetCharacter.location ? 'correct' : 'incorrect',
                origins: guessedCharacter.origins === targetCharacter.origins ? 'correct' : 'incorrect',
                role: guessedCharacter.role === targetCharacter.role ? 'correct' : 'incorrect',
                tags: arraysEqual(parseTagsArray(guessedCharacter.tags), parseTagsArray(targetCharacter.tags)) ? 'correct' : 'incorrect'
            }
        });

        updateGuessHistory();
        attemptCountDiv.textContent = guessHistory.length;

        // Vérifier si c'est correct
        if (guessedCharacter.id === targetCharacter.id) {
            gameWon = true;
            input.disabled = true;
            showMessage(`🎉 Félicitations ! Vous avez trouvé ${targetCharacter.alias} en ${guessHistory.length} tentative(s) !`, 'success');
            showVictoryAnimation();
        } else {
            showMessage(`❌ Non, ce n'est pas ${guessedCharacter.alias}. Regardez les indices de couleur !`, 'error');
        }

        input.value = '';
        searchPortrait.style.display = 'none';

    } catch (error) {
        showMessage('❌ Erreur de connexion', 'error');
        console.error('Erreur:', error);
    } finally {
        showLoading(false);
    }
}

// Mettre à jour l'historique des tentatives avec animation en cascade
function updateGuessHistory() {
    const newGuessIndex = guessHistory.length - 1;

    // Inverser l'ordre pour afficher les plus récentes en haut
    const reversedHistory = [...guessHistory].reverse();

    historyDiv.innerHTML = reversedHistory.map((guess, index) => {
        const comp = guess.comparison;
        const char = guess.character;

        const isWin = char.id === targetCharacter.id;
        const characterClass = isWin ? 'correct' : 'character';
        // La nouvelle tentative est maintenant à l'index 0 après l'inversion
        const isNewGuess = index === 0;

        // Construire le chemin du portrait à partir du character_id
        const portraitSrc = `http://localhost:5001/portraits/Portrait_${char.character_id}.png`;

        return `
                    <div class="guess-row" style="animation: slideIn 0.5s ease-out;">
                        <div class="cell portrait-cell ${isNewGuess ? 'new-cell' : ''}">
                            <img src="${portraitSrc}" alt="${char.alias}" class="portrait" 
                                 onerror="this.style.display='none'">
                        </div>
                        <div class="cell ${characterClass} ${isNewGuess ? 'new-cell' : ''}">${char.alias}</div>
                        <div class="cell ${comp.alignment} ${isNewGuess ? 'new-cell' : ''}">${char.alignment}</div>
                        <div class="cell ${comp.location} ${isNewGuess ? 'new-cell' : ''}">${char.location}</div>
                        <div class="cell ${comp.origins} ${isNewGuess ? 'new-cell' : ''}">${char.origins}</div>
                        <div class="cell ${comp.role} ${isNewGuess ? 'new-cell' : ''}">${char.role}</div>
                        <div class="cell ${comp.tags} ${isNewGuess ? 'new-cell' : ''}">${char.tags}</div>
                    </div>
                `;
    }).join('');

    // Supprimer la classe new-cell après l'animation
    setTimeout(() => {
        document.querySelectorAll('.new-cell').forEach(cell => {
            cell.classList.remove('new-cell');
        });
    }, 1000);
}

// Utilitaires
function parseTagsArray(tagsString) {
    if (!tagsString || tagsString.trim() === '') return [];
    return tagsString.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0);
}

function arraysEqual(a, b) {
    if (a.length !== b.length) return false;
    const sortedA = [...a].sort();
    const sortedB = [...b].sort();
    return sortedA.every((val, i) => val === sortedB[i]);
}

function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';

    setTimeout(() => {
        if (messageDiv.textContent === text) {
            messageDiv.style.display = 'none';
        }
    }, 5000);
}

// Animation de victoire
function showVictoryAnimation() {
    const victoryDiv = document.createElement('div');
    victoryDiv.className = 'victory-animation';
    victoryDiv.id = 'victoryAnimation';

    // Construire le chemin du portrait à partir du character_id
    const portraitSrc = `http://localhost:5001/portraits/Portrait_${targetCharacter.character_id}.png`;

    victoryDiv.innerHTML = `
                <div class="victory-content">
                    <div class="victory-title">🎉 VICTOIRE ! 🎉</div>
                    <img src="${portraitSrc}" alt="${targetCharacter.alias}" class="victory-portrait" 
                         onerror="this.style.display='none'">
                    <div class="victory-message">
                        Vous avez trouvé <strong>${targetCharacter.alias}</strong><br>
                        en ${guessHistory.length} tentative${guessHistory.length > 1 ? 's' : ''} !
                    </div>
                    <button class="victory-button" onclick="restartGame()">🔄 Recommencer</button>
                </div>
            `;

    // Ajouter des confettis
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'victory-confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.animationDelay = Math.random() * 3 + 's';
        confetti.style.backgroundColor = ['#FCD34D', '#10B981', '#F59E0B', '#3B82F6'][Math.floor(Math.random() * 4)];
        victoryDiv.appendChild(confetti);
    }

    document.body.appendChild(victoryDiv);

    // L'animation ne se supprime plus automatiquement
}

// Fonction pour recommencer le jeu
function restartGame() {
    // Supprimer l'animation de victoire
    const victoryDiv = document.getElementById('victoryAnimation');
    if (victoryDiv) {
        victoryDiv.remove();
    }

    // Relancer une nouvelle partie
    startNewGame();
}

// Initialiser le jeu
window.addEventListener('load', async () => {
    await loadCharacters();
    startNewGame();
});