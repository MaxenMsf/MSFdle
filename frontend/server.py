#!/usr/bin/env python3
"""
Serveur HTTP simple pour servir les fichiers du frontend MSFdle
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8080
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Ajouter les headers CORS pour permettre les requêtes vers localhost:5000
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    print(f"🚀 Démarrage du serveur HTTP sur le port {PORT}")
    print(f"📁 Répertoire servi: {DIRECTORY}")
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"✅ Serveur démarré sur http://localhost:{PORT}")
        print(f"🎯 Accédez au jeu via: http://localhost:{PORT}/test_game.html")
        print(f"🔧 Test simple via: http://localhost:{PORT}/test_simple.html")
        print(f"⏹️  Appuyez sur Ctrl+C pour arrêter")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du serveur...")

if __name__ == "__main__":
    main()
