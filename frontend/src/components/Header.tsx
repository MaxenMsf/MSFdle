import React from 'react';
import { Shield, Zap, Target, Heart, Sword } from 'lucide-react';

interface HeaderProps {
  onNewGame: () => void;
  gameWon: boolean;
  attemptCount: number;
}

const Header: React.FC<HeaderProps> = ({ onNewGame, gameWon, attemptCount }) => {
  return (
    <header className="bg-white/10 backdrop-blur-md border-b border-white/20 px-6 py-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Shield className="w-8 h-8 text-marvel-red" />
            <h1 className="text-2xl font-bold text-white">
              MSF<span className="text-marvel-gold">dle</span>
            </h1>
          </div>
          
          <div className="hidden md:flex items-center space-x-4 text-sm text-white/80">
            <div className="flex items-center space-x-1">
              <Target className="w-4 h-4" />
              <span>Devinez le personnage</span>
            </div>
            <div className="w-px h-4 bg-white/30"></div>
            <div className="flex items-center space-x-1">
              <Zap className="w-4 h-4" />
              <span>Marvel Strike Force</span>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-white/90 text-sm">
            <span className="font-medium">Tentatives: </span>
            <span className={`font-bold ${gameWon ? 'text-green-400' : 'text-white'}`}>
              {attemptCount}
            </span>
          </div>
          
          <button
            onClick={onNewGame}
            className="bg-marvel-red hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2"
          >
            <Heart className="w-4 h-4" />
            <span>Nouvelle Partie</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
