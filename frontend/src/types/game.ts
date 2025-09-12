export interface Character {
  id: number;
  alias: string;
  alignment: string; // Hero/Vilain
  location: string; // Ville/Mondial/Cosmique
  origin1: string;
  origin2?: string;
  role: string; // Support/Cogneur/Manipulateur/Protecteur/Tireur
  tags?: string[]; // Tags optionnels
}

export interface GuessResult {
  character: Character;
  correct: boolean;
  comparison: {
    alignment: ComparisonResult;
    location: ComparisonResult;
    origin1: ComparisonResult;
    origin2: ComparisonResult;
    role: ComparisonResult;
    tags: ComparisonResult;
  };
}

export type ComparisonResult = 'correct' | 'partial' | 'incorrect';

export interface GameState {
  targetCharacter: Character | null;
  guesses: GuessResult[];
  gameWon: boolean;
  attemptCount: number;
}

export interface APIResponse<T> {
  data?: T;
  error?: string;
}
