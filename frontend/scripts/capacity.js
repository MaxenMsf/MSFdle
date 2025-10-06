let current = null;
let revealed = 1;
let allCharacters = [];
let allCapacities = [];
let guessedCharacters = [];
let rotation = 0;

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

async function fetchAllCapacities() {
    allCapacities = files.map(filename => {
        // Extraction du nom du perso après ICON_ABILITY_ et avant le prochain _
        const match = filename.match(/^ICON_ABILITY_([A-Z0-9]+)/);
        let raw = match ? match[1] : filename;
        // On cherche le personnage correspondant dans allCharacters (character_id en majuscules, sans ponctuation)
        let char = allCharacters.find(c => c.character_id && c.character_id.toUpperCase().replace(/[^A-Z0-9]/g, '') === raw);
        return {
            icon: `/capacites/${filename}`,
            character_id: char ? char.character_id : raw,
            alias: char ? char.alias : raw
        };
    });
}

async function fetchRandomCapacity() {
    // Choisit un personnage aléatoire
    if (!allCharacters.length) return null;
    const idx = Math.floor(Math.random() * allCharacters.length);
    const char = allCharacters[idx];
    // Détermine si c'est un serviteur (ajuste la logique selon ta base)
    const isServiteur = /Control_|Dmg_|Support_|Tank_/i.test(char.character_id);
    // Choix du type de capacité
    const types = isServiteur ? ['BASIC', 'SPECIAL', 'PASSIVE'] : ['BASIC', 'SPECIAL', 'ULTIMATE', 'PASSIVE'];
    const type = types[Math.floor(Math.random() * types.length)];
    // Construit le nom de fichier
    const filename = `ICON_ABILITY_${char.character_id.toUpperCase()}_${type}.png`;
    return {
        icon: `/capacites/${filename}`,
        character_id: char.character_id,
        alias: char.alias,
        type: type
    };
}

async function fetchData() {
    current = await fetchRandomCapacity();
    rotation = [0, 90, 180, 270][Math.floor(Math.random() * 4)];
    updateCapacityImage();
    document.getElementById('result').textContent = '';
    document.getElementById('guessInput').value = '';
    guessedCharacters = [];
    updateGuessedList();
}

function updateCapacityImage() {
    const img = document.getElementById('capacityImage');
    img.src = current ? current.icon : '';
    img.className = 'capacity-img bw rotated';
    img.style.setProperty('--rotation', rotation + 'deg');
    if (document.getElementById('colorSwitch').checked) {
        img.classList.remove('bw');
        img.classList.add('colored');
    } else {
        img.classList.add('bw');
        img.classList.remove('colored');
    }
    if (document.getElementById('rotationSwitch').checked) {
        img.classList.add('rotated');
    } else {
        img.classList.remove('rotated');
        img.style.setProperty('--rotation', '0deg');
    }
}

document.getElementById('rotationSwitch').addEventListener('change', updateCapacityImage);
document.getElementById('colorSwitch').addEventListener('change', updateCapacityImage);

function nextCapacity() {
    fetchData();
}

function updateGuessedList() {
    const guessedListDiv = document.getElementById('guessedList');
    if (!guessedListDiv) return;
    if (guessedCharacters.length === 0) {
        guessedListDiv.innerHTML = '';
        return;
    }
    const reversed = [...guessedCharacters].reverse();
    guessedListDiv.innerHTML = reversed.map(char => {
        const portrait = `/portraits/Portrait_${char.character_id}.png`;
        return `<div style="display:inline-flex;align-items:center;margin:0 12px 12px 0;padding:6px 12px;background:#181c2f;border-radius:12px;box-shadow:0 2px 8px #0003;">
            <img src="${portrait}" alt="${char.alias}" style="width:32px;height:32px;object-fit:cover;border-radius:50%;margin-right:10px;box-shadow:0 2px 8px #0006;">
            <span style="color:#fff;font-weight:500;">${char.alias}</span>
        </div>`;
    }).join('');
}

function submitGuess() {
    if (document.getElementById('victoryAnimation')) return;
    const guess = document.getElementById('guessInput').value.trim().toLowerCase();
    let guessedChar = allCharacters.find(char => char.alias.toLowerCase() === guess);
    if (!guessedChar && guess.length > 0) {
        guessedChar = allCharacters.find(char => char.alias.toLowerCase().replace(/[^a-z0-9]/g, '') === guess.replace(/[^a-z0-9]/g, ''));
    }
    if (guessedChar && !guessedCharacters.some(c => c.character_id === guessedChar.character_id)) {
        guessedCharacters.push({ character_id: guessedChar.character_id, alias: guessedChar.alias });
        updateGuessedList();
    }
    if (guessedChar && current && guessedChar.character_id === current.character_id) {
        showVictoryAnimationCapacity();
        document.getElementById('guessInput').value = '';
        updateSearchPortrait('');
        return;
    } else {
        document.getElementById('result').textContent = 'Raté !';
        document.getElementById('guessInput').value = '';
        updateSearchPortrait('');
    }
}

function showVictoryAnimationCapacity() {
    const victoryDiv = document.createElement('div');
    victoryDiv.className = 'victory-animation';
    victoryDiv.id = 'victoryAnimation';
    const alias = current.alias || current.name;
    const portraitSrc = `portraits/Portrait_${current.character_id}.png`;
    // Détection serviteur
    const isServiteur = /Control_|Dmg_|Support_|Tank_/i.test(current.character_id);
    // Boutons de choix
    // ...existing code...
    // Boutons de choix
    const types = isServiteur ? ['BASIC', 'SPECIAL', 'PASSIVE'] : ['BASIC', 'SPECIAL', 'ULTIMATE', 'PASSIVE'];
    const typeLabels = {
        'BASIC': 'Basique',
        'SPECIAL': 'Spécial',
        'ULTIMATE': 'Ultime',
        'PASSIVE': 'Passif'
    };
    const displayOrder = ['BASIC', 'SPECIAL', 'ULTIMATE', 'PASSIVE'];
    const orderedTypes = displayOrder.filter(t => types.includes(t));
    victoryDiv.innerHTML = `
        <div class="victory-content">
            <div class="victory-title">🎉 VICTOIRE ! 🎉</div>
            <img src="${portraitSrc}" alt="${alias}" class="victory-portrait" onerror="this.style.display='none'">
            <div class="victory-message">
                Vous avez trouvé <strong>${alias}</strong> !<br><br>
                <span>À quel type de capacité correspond cette icône ?</span>
                <div class="capacity-box" id="capacityBox">
                    <img id="capacityImage" src="${current.icon}" alt="Capacité" class="capacity-img rotated">
                </div>
                <div id="capacityTypeChoices" style="margin:18px 0 0 0;display:flex;gap:12px;flex-wrap:wrap;justify-content:center;"></div>
                <div id="capacityTypeResult" style="margin-top:14px;font-weight:700;font-size:1.15em;"></div>
            </div>
            <button class="victory-button" onclick="restartCapacityGame()" style="margin-top:18px;">🔄 Recommencer</button>
        </div>
    `;
    document.body.appendChild(victoryDiv);
    const choicesDiv = document.getElementById('capacityTypeChoices');
    orderedTypes.forEach(type => {
        const btn = document.createElement('button');
        btn.textContent = typeLabels[type];
        btn.className = 'victory-type-btn';
        btn.style.background = 'linear-gradient(90deg,#3b82f6 0%,#9333ea 100%)';
        btn.style.color = '#fff';
        btn.style.fontWeight = '600';
        btn.style.fontSize = '1em';
        btn.style.border = 'none';
        btn.style.borderRadius = '8px';
        btn.style.padding = '10px 22px';
        btn.style.cursor = 'pointer';
        btn.style.boxShadow = '0 2px 8px #0003';
        btn.style.transition = 'background 0.2s,transform 0.2s';
        btn.onmouseover = () => btn.style.background = 'linear-gradient(90deg,#2563eb 0%,#7c3aed 100%)';
        btn.onmouseout = () => btn.style.background = 'linear-gradient(90deg,#3b82f6 0%,#9333ea 100%)';
        btn.onclick = function () {
            const resultDiv = document.getElementById('capacityTypeResult');
            if (type === current.type) {
                resultDiv.textContent = 'Bravo, bonne réponse !';
                resultDiv.style.color = '#22d3ee'; // Cyan bien visible
                resultDiv.style.textShadow = '0 2px 8px #000a';
            } else {
                resultDiv.textContent = `Raté ! C’était "${typeLabels[current.type]}".`;
                resultDiv.style.color = '#F43F5E';
                resultDiv.style.textShadow = 'none';
            }
            Array.from(choicesDiv.children).forEach(b => b.disabled = true);
        };
        choicesDiv.appendChild(btn);
    });
}

function restartCapacityGame() {
    const victoryDiv = document.getElementById('victoryAnimation');
    if (victoryDiv) victoryDiv.remove();
    guessedCharacters = [];
    updateGuessedList();
    nextCapacity();
}

// Suggestions avec portraits (logique emoji)
const input = document.getElementById('guessInput');
const suggestions = document.getElementById('suggestions');
input.addEventListener('input', (e) => {
    const value = e.target.value.trim();
    showSuggestions(value);
    updateSearchPortrait(value);
});
input.addEventListener('focus', (e) => {
    showSuggestions(e.target.value.trim());
    updateSearchPortrait(e.target.value.trim());
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
    const excludedIds = guessedCharacters.map(c => c.character_id);
    const filtered = allCharacters.filter(char => char.alias.toLowerCase().includes(searchTerm) && !excludedIds.includes(char.character_id));
    if (filtered.length === 0) {
        suggestions.style.display = 'none';
        return;
    }
    suggestions.innerHTML = filtered.map(char => {
        let portraitName = `/portraits/Portrait_${char.character_id}.png`;
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

// Portrait dans la barre de recherche
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
        const portraitSrc = `/portraits/Portrait_${match.character_id}.png`;
        searchPortrait.src = portraitSrc;
        searchPortrait.style.display = 'block';
        searchPortrait.onerror = () => {
            searchPortrait.style.display = 'none';
        };
    } else {
        searchPortrait.style.display = 'none';
    }
}

window.onload = async function () {
    await fetchAllCharacters();
    fetchData();
};
