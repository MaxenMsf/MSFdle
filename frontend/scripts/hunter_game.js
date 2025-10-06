// Configuration du jeu
const config = {
    initialSpeed: 2,
    speedIncrement: 0.3,
    speedIncreaseInterval: 5000, // Augmente la vitesse toutes les 5 secondes
    maxEntities: 5,
    spawnInterval: 2000, // Nouvelle entité toutes les 2 secondes
    entitySize: 200, // Taille agrandie pour Iron Man
    lives: 3,
    spriteWidth: 246,  // Largeur d'une frame du sprite Iron Man
    spriteHeight: 118, // Hauteur d'une frame du sprite Iron Man
    spriteFrames: 3,   // Nombre de frames dans le sprite
    animationSpeed: 150 // Millisecondes entre chaque frame
};

// État du jeu
let gameState = {
    score: 0,
    lives: config.lives,
    speed: config.initialSpeed,
    entities: [],
    isPlaying: false,
    canvas: null,
    ctx: null,
    animationId: null,
    lastSpawnTime: 0,
    lastSpeedIncreaseTime: 0,
    backgroundMusic: null,
    snapSound: null,
    ironManSprite: null,
    customCursor: null
};

// Classe pour représenter une entité (Iron Man volant)
class Entity {
    constructor(canvas) {
        this.canvas = canvas;
        this.size = config.entitySize;
        this.x = -this.size;
        this.y = Math.random() * (canvas.height - this.size);
        this.speed = gameState.speed;
        this.currentFrame = 0;
        this.lastFrameTime = Date.now();
    }

    update() {
        this.x += this.speed;
        
        // Animation du sprite
        const now = Date.now();
        if (now - this.lastFrameTime > config.animationSpeed) {
            this.currentFrame = (this.currentFrame + 1) % config.spriteFrames;
            this.lastFrameTime = now;
        }
        
        return this.x < this.canvas.width + this.size;
    }

    draw(ctx) {
        if (gameState.ironManSprite && gameState.ironManSprite.complete) {
            // Dessiner la frame actuelle du sprite
            const frameX = this.currentFrame * config.spriteWidth;
            ctx.drawImage(
                gameState.ironManSprite,
                frameX, 0, // Position source dans le sprite sheet
                config.spriteWidth, config.spriteHeight, // Taille source
                this.x, this.y, // Position destination
                this.size, this.size * (config.spriteHeight / config.spriteWidth) // Taille destination (proportionnelle)
            );
        } else {
            // Fallback si l'image ne charge pas
            ctx.fillStyle = '#FFD700';
            ctx.fillRect(this.x, this.y, this.size, this.size * 0.5);
            ctx.strokeStyle = '#FF0000';
            ctx.lineWidth = 3;
            ctx.strokeRect(this.x, this.y, this.size, this.size * 0.5);
        }
    }

    isClicked(mouseX, mouseY) {
        const height = this.size * (config.spriteHeight / config.spriteWidth);
        return mouseX >= this.x && 
               mouseX <= this.x + this.size && 
               mouseY >= this.y && 
               mouseY <= this.y + height;
    }
}

// Initialisation du jeu
function initGame() {
    gameState.canvas = document.getElementById('gameCanvas');
    gameState.ctx = gameState.canvas.getContext('2d');
    gameState.customCursor = document.getElementById('customCursor');
    
    // Masquer le curseur personnalisé au démarrage (on est dans le menu)
    if (gameState.customCursor) {
        gameState.customCursor.classList.add('hidden');
    }
    
    // Charger le sprite Iron Man
    gameState.ironManSprite = new Image();
    gameState.ironManSprite.src = 'hunter/sprites/ironman.png';
    
    // Charger la musique de fond
    gameState.backgroundMusic = new Audio('hunter/music/Avengers Theme 8 bit.ogg');
    gameState.backgroundMusic.loop = true;
    gameState.backgroundMusic.volume = 0.3;
    
    // Charger le son du snap
    gameState.snapSound = new Audio('hunter/music/snap.ogg');
    gameState.snapSound.volume = 0.5;
    
    // Ajuster la taille du canvas
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Gérer le curseur personnalisé
    document.addEventListener('mousemove', updateCursorPosition);
    document.addEventListener('mousedown', onMouseDown);
    document.addEventListener('mouseup', onMouseUp);
    
    // Événements de clic
    gameState.canvas.addEventListener('click', handleClick);
    gameState.canvas.addEventListener('click', createClickEffect);
}

function updateCursorPosition(e) {
    if (gameState.customCursor) {
        gameState.customCursor.style.left = e.clientX + 'px';
        gameState.customCursor.style.top = e.clientY + 'px';
    }
}

function onMouseDown() {
    if (gameState.customCursor) {
        gameState.customCursor.classList.add('clicking');
    }
}

function onMouseUp() {
    if (gameState.customCursor) {
        gameState.customCursor.classList.remove('clicking');
    }
}

function resizeCanvas() {
    const hud = document.querySelector('.hud');
    gameState.canvas.width = window.innerWidth;
    gameState.canvas.height = window.innerHeight - hud.offsetHeight;
}

function startGame() {
    // Réinitialiser l'état
    gameState.score = 0;
    gameState.lives = config.lives;
    gameState.speed = config.initialSpeed;
    gameState.entities = [];
    gameState.isPlaying = true;
    gameState.lastSpawnTime = Date.now();
    gameState.lastSpeedIncreaseTime = Date.now();
    
    // Afficher le curseur personnalisé
    if (gameState.customCursor) {
        gameState.customCursor.classList.remove('hidden');
    }
    
    // Démarrer la musique
    if (gameState.backgroundMusic) {
        gameState.backgroundMusic.currentTime = 0;
        gameState.backgroundMusic.play().catch(e => console.log('Erreur lecture musique:', e));
    }
    
    // Cacher l'écran de démarrage
    document.getElementById('startScreen').classList.add('hidden');
    
    // Mettre à jour l'affichage
    updateHUD();
    
    // Démarrer la boucle de jeu
    gameLoop();
}

function gameLoop(timestamp) {
    if (!gameState.isPlaying) return;
    
    const now = Date.now();
    
    // Spawn de nouvelles entités
    if (now - gameState.lastSpawnTime > config.spawnInterval && 
        gameState.entities.length < config.maxEntities) {
        gameState.entities.push(new Entity(gameState.canvas));
        gameState.lastSpawnTime = now;
    }
    
    // Augmenter la vitesse progressivement
    if (now - gameState.lastSpeedIncreaseTime > config.speedIncreaseInterval) {
        gameState.speed += config.speedIncrement;
        gameState.lastSpeedIncreaseTime = now;
        
        // Mettre à jour la vitesse des entités existantes
        gameState.entities.forEach(entity => {
            entity.speed = gameState.speed;
        });
    }
    
    // Effacer le canvas
    gameState.ctx.clearRect(0, 0, gameState.canvas.width, gameState.canvas.height);
    
    // Mettre à jour et dessiner les entités
    gameState.entities = gameState.entities.filter(entity => {
        const stillAlive = entity.update();
        
        // Si l'entité sort de l'écran, on perd une vie
        if (!stillAlive) {
            loseLife();
        }
        
        entity.draw(gameState.ctx);
        return stillAlive;
    });
    
    gameState.animationId = requestAnimationFrame(gameLoop);
}

function handleClick(event) {
    if (!gameState.isPlaying) return;
    
    const rect = gameState.canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
    
    // Vérifier si on a cliqué sur une entité
    for (let i = gameState.entities.length - 1; i >= 0; i--) {
        if (gameState.entities[i].isClicked(mouseX, mouseY)) {
            // Retirer l'entité
            gameState.entities.splice(i, 1);
            
            // Augmenter le score
            gameState.score += 10;
            updateHUD();
            
            // Jouer le son du snap
            if (gameState.snapSound) {
                gameState.snapSound.currentTime = 0;
                gameState.snapSound.play().catch(e => console.log('Erreur son:', e));
            }
            break;
        }
    }
}

function createClickEffect(event) {
    const effect = document.createElement('div');
    effect.className = 'click-effect';
    effect.style.left = (event.clientX - 17.5) + 'px'; // Ajusté pour le nouveau curseur
    effect.style.top = (event.clientY - 34.5) + 'px';
    document.body.appendChild(effect);
    
    setTimeout(() => {
        effect.remove();
    }, 500);
}

function loseLife() {
    gameState.lives--;
    updateHUD();
    
    if (gameState.lives <= 0) {
        endGame();
    }
}

function updateHUD() {
    document.getElementById('score').textContent = gameState.score;
    
    const heartsDisplay = '❤️'.repeat(Math.max(0, gameState.lives)) + 
                          '🖤'.repeat(Math.max(0, config.lives - gameState.lives));
    document.getElementById('lives').textContent = heartsDisplay;
}

function endGame() {
    gameState.isPlaying = false;
    cancelAnimationFrame(gameState.animationId);
    
    // Masquer le curseur personnalisé
    if (gameState.customCursor) {
        gameState.customCursor.classList.add('hidden');
    }
    
    // Arrêter la musique
    if (gameState.backgroundMusic) {
        gameState.backgroundMusic.pause();
    }
    
    // Afficher l'écran de game over
    document.getElementById('finalScore').textContent = gameState.score;
    document.getElementById('gameOver').classList.remove('hidden');
}

function restartGame() {
    document.getElementById('gameOver').classList.add('hidden');
    startGame();
}

// Initialiser le jeu au chargement de la page
window.addEventListener('load', initGame);
