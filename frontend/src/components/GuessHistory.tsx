import React from 'react';
import { GuessResult, ComparisonResult } from '../types/game';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';

interface GuessHistoryProps {
  guesses: GuessResult[];
}

const ComparisonCell: React.FC<{ 
  value: string | null; 
  result: ComparisonResult; 
  label: string;
}> = ({ value, result, label }) => {
  const getColorClass = () => {
    switch (result) {
      case 'correct': return 'bg-green-500';
      case 'partial': return 'bg-yellow-500';
      case 'incorrect': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getIcon = () => {
    switch (result) {
      case 'correct': return <CheckCircle className="w-4 h-4" />;
      case 'partial': return <AlertCircle className="w-4 h-4" />;
      case 'incorrect': return <XCircle className="w-4 h-4" />;
      default: return null;
    }
  };

  return (
    <div className={`${getColorClass()} p-3 rounded-lg text-white text-center min-h-[80px] flex flex-col justify-center items-center space-y-1`}>
      <div className="flex items-center space-x-1">
        {getIcon()}
        <span className="text-xs font-medium opacity-80">{label}</span>
      </div>
      <div className="font-medium text-sm">{value || 'N/A'}</div>
    </div>
  );
};

const GuessHistory: React.FC<GuessHistoryProps> = ({ guesses }) => {
  if (guesses.length === 0) {
    return (
      <div className="text-center text-white/60 py-8">
        <div className="text-4xl mb-4">🤔</div>
        <p>Aucune tentative pour le moment.</p>
        <p className="text-sm mt-2">Commencez à deviner !</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
        <span>Historique des tentatives ({guesses.length})</span>
      </h3>
      
      {/* En-têtes */}
      <div className="grid grid-cols-6 gap-2 mb-2">
        <div className="text-white/80 text-sm font-medium text-center">Personnage</div>
        <div className="text-white/80 text-sm font-medium text-center">Alignement</div>
        <div className="text-white/80 text-sm font-medium text-center">Localisation</div>
        <div className="text-white/80 text-sm font-medium text-center">Origine 1</div>
        <div className="text-white/80 text-sm font-medium text-center">Origine 2</div>
        <div className="text-white/80 text-sm font-medium text-center">Rôle</div>
      </div>

      {/* Tentatives */}
      <div className="space-y-3">
        {guesses.map((guess, index) => (
          <div key={index} className="grid grid-cols-6 gap-2 fade-in">
            {/* Nom du personnage */}
            <div className={`p-3 rounded-lg text-white text-center min-h-[80px] flex flex-col justify-center items-center ${
              guess.correct ? 'bg-green-500 pulse-animation' : 'bg-blue-600'
            }`}>
              <div className="font-bold text-sm">{guess.character.alias}</div>
              {guess.correct && (
                <div className="text-xs mt-1 opacity-80">🎉 Correct!</div>
              )}
            </div>

            {/* Comparaisons */}
            <ComparisonCell
              value={guess.character.alignment}
              result={guess.comparison.alignment}
              label="Alignement"
            />
            <ComparisonCell
              value={guess.character.location}
              result={guess.comparison.location}
              label="Localisation"
            />
            <ComparisonCell
              value={guess.character.origin1}
              result={guess.comparison.origin1}
              label="Origine 1"
            />
            <ComparisonCell
              value={guess.character.origin2}
              result={guess.comparison.origin2}
              label="Origine 2"
            />
            <ComparisonCell
              value={guess.character.role}
              result={guess.comparison.role}
              label="Rôle"
            />
          </div>
        ))}
      </div>

      {/* Légende */}
      <div className="mt-6 p-4 bg-white/5 rounded-lg">
        <h4 className="text-white font-medium mb-3">Légende:</h4>
        <div className="flex flex-wrap gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-green-500 rounded"></div>
            <span className="text-white/80">Correct</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-yellow-500 rounded"></div>
            <span className="text-white/80">Partiellement correct</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-red-500 rounded"></div>
            <span className="text-white/80">Incorrect</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GuessHistory;
