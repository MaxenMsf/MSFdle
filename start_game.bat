@echo off
echo 🎯 Lancement de MSFdle - Marvel Strike Force Wordle
echo ================================================
echo.

echo 📂 Verification des fichiers...
if not exist "backend\app.py" (
    echo ❌ Fichier backend non trouve!
    pause
    exit /b 1
)

if not exist "data\msfdle.db" (
    echo ❌ Base de donnees non trouvee!
    pause
    exit /b 1
)

echo ✅ Fichiers trouves

echo.
echo 🚀 Demarrage du serveur backend...
cd backend
start "MSFdle Backend" python app.py

echo ⏳ Attente du demarrage du serveur...
timeout /t 3 /nobreak >nul

echo.
echo 🎮 Ouverture du jeu dans le navigateur...
cd ..\frontend
start "" "test_game.html"

echo.
echo ✅ MSFdle lance avec succes!
echo.
echo 📋 Instructions:
echo    - Le serveur backend tourne sur http://127.0.0.1:5000
echo    - Le jeu s'ouvre dans votre navigateur
echo    - Pour l'administration: ouvrez admin_tags.html
echo.
echo 🔄 Pour relancer: executez ce script
echo 🛑 Pour arreter: fermez la fenetre du serveur backend
echo.
pause
