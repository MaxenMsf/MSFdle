import React, { useState, useEffect } from 'react';
import { Character, GuessResult, GameState } from './types/game';
import { gameAPI } from './services/api';
import Header from './components/Header';
import SearchInput from './components/SearchInput';
import GuessHistory from './components/GuessHistory';
import { Trophy, AlertCircle } from 'lucide-react';

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>({
    targetCharacter: null,
    guesses: [],
    gameWon: false,
    attemptCount: 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialiser une nouvelle partie
  const startNewGame = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const randomCharacter = await gameAPI.getRandomCharacter();
      setGameState({
        targetCharacter: randomCharacter,
        guesses: [],
        gameWon: false,
        attemptCount: 0,
      });
    } catch (err) {
      setError('Impossible de démarrer une nouvelle partie. Vérifiez votre connexion.');
      console.error('Erreur nouvelle partie:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Gérer une tentative
  const handleGuess = async (characterName: string) => {
    if (!gameState.targetCharacter || gameState.gameWon) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await gameAPI.checkGuess(characterName, gameState.targetCharacter.id);
      
      setGameState(prev => ({
        ...prev,
        guesses: [...prev.guesses, result],
        gameWon: result.correct,
        attemptCount: prev.attemptCount + 1,
      }));

      // Si gagné, afficher un message de félicitations
      if (result.correct) {
        setTimeout(() => {
          alert(`🎉 Félicitations ! Vous avez trouvé ${result.character.alias} en ${gameState.attemptCount + 1} tentatives !`);
        }, 500);
      }
    } catch (err) {
      setError('Erreur lors de la vérification. Vérifiez le nom du personnage.');
      console.error('Erreur tentative:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Rechercher des personnages pour l'autocomplétion
  const searchCharacters = async (query: string): Promise<string[]> => {
    try {
      return await gameAPI.searchCharacters(query);
    } catch (error) {
      console.error('Erreur recherche:', error);
      return [];
    }
  };

  // Démarrer la première partie au chargement
  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
      <Header 
        onNewGame={startNewGame}
        gameWon={gameState.gameWon}
        attemptCount={gameState.attemptCount}
      />

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Zone de jeu principale */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white mb-4">
            🎯 Devinez le personnage Marvel Strike Force
          </h2>
          <p className="text-white/80 text-lg">
            Utilisez les indices de couleur pour trouver le personnage mystère !
          </p>
        </div>

        {/* Message d'erreur */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center space-x-3 max-w-2xl mx-auto">
            <AlertCircle className="w-5 h-5 text-red-400" />
            <span className="text-red-200">{error}</span>
          </div>
        )}

        {/* État de chargement */}
        {isLoading && (
          <div className="text-center mb-6">
            <div className="inline-flex items-center space-x-2 text-white/80">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Chargement...</span>
            </div>
          </div>
        )}

        {/* Zone de recherche */}
        <div className="mb-8">
          <SearchInput
            onGuess={handleGuess}
            searchCharacters={searchCharacters}
            disabled={isLoading || gameState.gameWon || !gameState.targetCharacter}
          />
        </div>

        {/* Message de victoire */}
        {gameState.gameWon && (
          <div className="mb-8 p-6 bg-green-500/20 border border-green-500/50 rounded-lg text-center max-w-2xl mx-auto">
            <Trophy className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-white mb-2">🎉 Félicitations !</h3>
            <p className="text-green-200">
              Vous avez trouvé <strong>{gameState.targetCharacter?.alias}</strong> en {gameState.attemptCount} tentatives !
            </p>
            <button
              onClick={startNewGame}
              className="mt-4 bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Rejouer
            </button>
          </div>
        )}

        {/* Informations sur le personnage cible (pour le développement) */}
        {process.env.NODE_ENV === 'development' && gameState.targetCharacter && (
          <div className="mb-6 p-4 bg-yellow-500/20 border border-yellow-500/50 rounded-lg max-w-2xl mx-auto">
            <p className="text-yellow-200 text-sm">
              <strong>DEV:</strong> Personnage cible: {gameState.targetCharacter.alias} 
              ({gameState.targetCharacter.alignment}, {gameState.targetCharacter.location}, {gameState.targetCharacter.role})
            </p>
          </div>
        )}

        {/* Historique des tentatives */}
        <div className="mt-8">
          <GuessHistory guesses={gameState.guesses} />
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-white/10">
        <div className="max-w-6xl mx-auto px-6 text-center text-white/60">
          <p className="mb-2">MSFdle - Inspired by Wordle, made for Marvel Strike Force fans</p>
          <p className="text-sm">
            Créé avec ❤️ pour la communauté Marvel Strike Force
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;
