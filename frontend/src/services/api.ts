import axios from 'axios';
import { Character, GuessResult } from '../types/game';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const gameAPI = {
  // Récupérer tous les personnages
  async getAllCharacters(): Promise<Character[]> {
    const response = await api.get<Character[]>('/characters');
    return response.data;
  },

  // Récupérer un personnage aléatoire
  async getRandomCharacter(): Promise<Character> {
    const response = await api.get<Character>('/random-character');
    return response.data;
  },

  // Rechercher des personnages (autocomplétion)
  async searchCharacters(query: string): Promise<string[]> {
    const response = await api.get<string[]>('/search', {
      params: { q: query }
    });
    return response.data;
  },

  // Vérifier une devinette
  async checkGuess(guess: string, targetId: number): Promise<GuessResult> {
    const response = await api.post<GuessResult>('/guess', {
      guess,
      target_id: targetId
    });
    return response.data;
  },

  // Vérifier l'état de l'API
  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await api.get('/health');
    return response.data;
  }
};

// Intercepteur pour la gestion d'erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    
    if (error.response) {
      // Erreur de réponse du serveur
      throw new Error(error.response.data?.error || 'Erreur du serveur');
    } else if (error.request) {
      // Erreur de réseau
      throw new Error('Impossible de contacter le serveur');
    } else {
      // Autre erreur
      throw new Error('Une erreur inattendue s\'est produite');
    }
  }
);
