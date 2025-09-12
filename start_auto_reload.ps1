# MSFdle Auto-Reload Script
# Lance le serveur Flask avec auto-reload et surveille les modifications

param(
    [switch]$Verbose = $false,
    [int]$Port = 5001
)

# Couleurs pour les messages
$colors = @{
    Info = "Cyan"
    Success = "Green" 
    Warning = "Yellow"
    Error = "Red"
}

function Write-ColorMessage {
    param([string]$Message, [string]$Type = "Info")
    Write-Host $Message -ForegroundColor $colors[$Type]
}

function Show-Banner {
    Clear-Host
    Write-Host "=" * 60 -ForegroundColor Magenta
    Write-Host "                  MSFDLE AUTO-RELOAD" -ForegroundColor Magenta
    Write-Host "=" * 60 -ForegroundColor Magenta
    Write-Host ""
}

function Test-Prerequisites {
    # Vérifier Python
    try {
        $pythonVersion = python --version 2>$null
        Write-ColorMessage "✅ Python détecté: $pythonVersion" "Success"
    }
    catch {
        Write-ColorMessage "❌ Python non trouvé. Installez Python d'abord." "Error"
        exit 1
    }
    
    # Vérifier structure du projet
    if (!(Test-Path "backend\app.py")) {
        Write-ColorMessage "❌ backend\app.py non trouvé. Lancez depuis le répertoire MSFdle." "Error"
        exit 1
    }
    
    Write-ColorMessage "✅ Structure du projet validée" "Success"
}

function Start-FlaskServer {
    Show-Banner
    
    Write-ColorMessage "🎮 Démarrage du serveur MSFdle..." "Info"
    Write-ColorMessage "🔄 Auto-reload Flask activé (debug=True)" "Info" 
    Write-ColorMessage "🌐 URL du jeu: http://127.0.0.1:$Port" "Success"
    Write-ColorMessage "📝 Surveillance des fichiers: .py, .html, .css, .js" "Info"
    Write-Host ""
    Write-ColorMessage "⚡ Modifiez vos fichiers - le serveur redémarrera automatiquement" "Warning"
    Write-ColorMessage "🛑 Appuyez sur Ctrl+C pour arrêter" "Warning"
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Magenta
    Write-Host ""
    
    # Changer vers le répertoire backend
    Set-Location "backend"
    
    # Variables d'environnement Flask
    $env:FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    
    try {
        # Lancer Flask avec auto-reload
        python app.py
    }
    catch {
        Write-ColorMessage "❌ Erreur lors du démarrage du serveur" "Error"
        Write-ColorMessage $_.Exception.Message "Error"
    }
    finally {
        Write-Host ""
        Write-ColorMessage "🛑 Serveur arrêté" "Warning"
        Set-Location ".."
    }
}

function Show-Help {
    Write-Host "Usage: .\start_auto_reload.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Verbose      Affichage détaillé"
    Write-Host "  -Port <num>   Port du serveur (défaut: 5001)"
    Write-Host "  -Help         Affiche cette aide"
    Write-Host ""
    Write-Host "Exemples:"
    Write-Host "  .\start_auto_reload.ps1"
    Write-Host "  .\start_auto_reload.ps1 -Port 8080"
    Write-Host "  .\start_auto_reload.ps1 -Verbose"
}

# Script principal
if ($args -contains "-Help" -or $args -contains "--help") {
    Show-Help
    exit 0
}

Write-Host "Initialisation du serveur MSFdle..." -ForegroundColor Cyan

# Vérifications préalables
Test-Prerequisites

# Démarrer le serveur
Start-FlaskServer