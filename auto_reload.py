#!/usr/bin/env python3
"""
Script de surveillance automatique pour MSFdle (version simple)
Surveille les modifications des fichiers et relance automatiquement le serveur
Version sans dépendances externes - utilise seulement les modules Python standard
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

class SimpleFileWatcher:
    def __init__(self):
        self.process = None
        self.watching = True
        self.file_timestamps = {}
        self.restart_delay = 2  # Délai en secondes avant redémarrage
        self.last_restart = 0
        
    def get_file_timestamp(self, filepath):
        """Récupère le timestamp de modification d'un fichier"""
        try:
            return os.path.getmtime(filepath)
        except:
            return 0
    
    def scan_files(self):
        """Scanne tous les fichiers pertinents"""
        extensions = ['.py', '.html', '.css', '.js', '.sql']
        directories = ['backend', 'frontend', 'data', 'database']
        
        files = []
        for directory in directories:
            if os.path.exists(directory):
                for ext in extensions:
                    pattern = f"**/*{ext}"
                    files.extend(Path(directory).glob(pattern))
        
        return [str(f) for f in files]
    
    def check_for_changes(self):
        """Vérifie s'il y a des modifications"""
        current_files = self.scan_files()
        changes_detected = False
        
        # Vérifier les fichiers existants
        for filepath in current_files:
            current_time = self.get_file_timestamp(filepath)
            
            if filepath in self.file_timestamps:
                if current_time > self.file_timestamps[filepath]:
                    print(f"📝 Modification détectée: {filepath}")
                    changes_detected = True
            
            self.file_timestamps[filepath] = current_time
        
        # Vérifier les fichiers supprimés
        for filepath in list(self.file_timestamps.keys()):
            if filepath not in current_files:
                print(f"🗑️ Fichier supprimé: {filepath}")
                del self.file_timestamps[filepath]
                changes_detected = True
        
        return changes_detected
    
    def start_server(self):
        """Démarre le serveur Flask"""
        if self.process:
            self.stop_server()
        
        print("🚀 Démarrage du serveur MSFdle...")
        try:
            # Démarrer le serveur Flask dans le répertoire backend
            self.process = subprocess.Popen([
                sys.executable, "app.py"
            ], cwd="backend")
            print(f"✅ Serveur démarré avec PID: {self.process.pid}")
            print("🌐 Jeu accessible sur: http://127.0.0.1:5001")
        except Exception as e:
            print(f"❌ Erreur lors du démarrage: {e}")
    
    def stop_server(self):
        """Arrête le serveur Flask"""
        if self.process:
            print("🛑 Arrêt du serveur...")
            try:
                self.process.terminate()
                # Attendre un maximum de 5 secondes
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()
                print("✅ Serveur arrêté")
            except Exception as e:
                print(f"⚠️ Erreur lors de l'arrêt: {e}")
            finally:
                self.process = None
    
    def restart_server(self):
        """Redémarre le serveur avec un délai anti-spam"""
        current_time = time.time()
        if current_time - self.last_restart < self.restart_delay:
            return
        
        self.last_restart = current_time
        print("🔄 Redémarrage du serveur...")
        self.start_server()
    
    def watch_files(self):
        """Surveille les fichiers en continu"""
        print("🔍 Surveillance des fichiers démarrée...")
        
        # Scan initial
        self.scan_files()
        for filepath in self.scan_files():
            self.file_timestamps[filepath] = self.get_file_timestamp(filepath)
        
        while self.watching:
            try:
                if self.check_for_changes():
                    self.restart_server()
                time.sleep(1)  # Vérifier toutes les secondes
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️ Erreur de surveillance: {e}")
                time.sleep(5)

def main():
    """Fonction principale"""
    print("🎮 MSFdle Auto-Reload (Version Simple)")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("backend/app.py"):
        print("❌ Erreur: backend/app.py non trouvé")
        print("📁 Assurez-vous d'être dans le répertoire MSFdle")
        sys.exit(1)
    
    watcher = SimpleFileWatcher()
    
    # Démarrer le serveur initial
    watcher.start_server()
    
    print("\n👁️ Surveillance active des répertoires:")
    directories = ['backend', 'frontend', 'data', 'database']
    for directory in directories:
        if os.path.exists(directory):
            print(f"   📁 {directory}/")
    
    print("\n🔍 Extensions surveillées: .py, .html, .css, .js, .sql")
    print("� Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Lancer la surveillance dans un thread séparé
        watch_thread = threading.Thread(target=watcher.watch_files)
        watch_thread.daemon = True
        watch_thread.start()
        
        # Attendre que l'utilisateur arrête
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé...")
        watcher.watching = False
        watcher.stop_server()
        print("✅ Auto-reload arrêté")

if __name__ == "__main__":
    main()