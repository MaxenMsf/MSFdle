@echo off
title MSFdle - Auto-Reload Server
color 0A

echo ========================================
echo     MSFDLE AUTO-RELOAD SERVER
echo ========================================
echo.
echo 🎮 Demarrage du serveur MSFdle...
echo 🔄 Auto-reload active avec Flask Debug
echo 🌐 Acces au jeu: http://127.0.0.1:5001
echo.
echo ⚡ Les modifications seront detectees automatiquement
echo 📝 Fichiers surveilles: .py, .html, .css, .js
echo.
echo 🛑 Appuyez sur Ctrl+C pour arreter
echo ========================================
echo.

cd /d "%~dp0"
cd backend

python app.py

pause