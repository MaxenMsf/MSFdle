import React, { useState, useRef } from 'react';
import { Search, User } from 'lucide-react';

interface SearchInputProps {
  onGuess: (characterName: string) => void;
  searchCharacters: (query: string) => Promise<string[]>;
  disabled?: boolean;
}

const SearchInput: React.FC<SearchInputProps> = ({ 
  onGuess, 
  searchCharacters, 
  disabled = false 
}) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleInputChange = async (value: string) => {
    setQuery(value);
    
    if (value.length >= 2) {
      setIsLoading(true);
      try {
        const results = await searchCharacters(value);
        setSuggestions(results);
        setShowSuggestions(true);
      } catch (error) {
        console.error('Erreur de recherche:', error);
        setSuggestions([]);
      }
      setIsLoading(false);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onGuess(query.trim());
      setQuery('');
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    onGuess(suggestion);
    setQuery('');
    setSuggestions([]);
    setShowSuggestions(false);
    inputRef.current?.blur();
  };

  return (
    <div className="relative w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => handleInputChange(e.target.value)}
            placeholder="Tapez le nom d'un personnage..."
            disabled={disabled}
            className="w-full pl-10 pr-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg text-white placeholder-white/60 focus:outline-none focus:border-marvel-gold focus:ring-2 focus:ring-marvel-gold/30 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          {isLoading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            </div>
          )}
        </div>
        
        <button
          type="submit"
          disabled={disabled || !query.trim()}
          className="mt-3 w-full bg-marvel-red hover:bg-red-600 disabled:bg-gray-600 disabled:cursor-not-allowed text-white py-2 px-4 rounded-lg font-medium transition-colors"
        >
          Deviner
        </button>
      </form>

      {/* Suggestions dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className="w-full px-4 py-2 text-left text-white hover:bg-white/20 transition-colors flex items-center space-x-2 first:rounded-t-lg last:rounded-b-lg"
            >
              <User className="w-4 h-4 text-gray-400" />
              <span>{suggestion}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchInput;
