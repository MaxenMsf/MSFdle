@echo off
echo 🚀 Demarrage du frontend MSFdle...
echo.

cd /d "%~dp0"

echo 📦 Installation des dependances...
call npm install

echo.
echo 🎯 Demarrage du serveur de developpement...
call npm run dev

pause
