@echo off
chcp 65001 >nul
title L'application pour que tu ne me demandes plus d'installer des musiques

echo.
echo 🎥 YouTube Downloader - Démarrage
echo =====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo 💡 Solutions:
    echo    1. Installer Python depuis https://python.org
    echo    2. Cocher "Add Python to PATH" lors de l'installation
    echo    3. Redémarrer l'ordinateur après installation
    echo.
    pause
    exit /b 1
)

REM Afficher la version de Python
echo ✅ Python détecté:
python --version
echo.

REM Vérifier si pip est disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip n'est pas disponible
    echo 💡 Réinstallez Python avec pip inclus
    pause
    exit /b 1
)

REM Mettre à jour pip
echo 🔧 Mise à jour de pip...
python -m pip install --upgrade pip --user >nul 2>&1

REM Lancer le script Python de démarrage
echo 🚀 Lancement de l'application...
echo.

python start.py

REM Si le script se termine avec une erreur
if errorlevel 1 (
    echo.
    echo ❌ L'application s'est fermée avec une erreur
    echo 💡 Vérifiez les messages ci-dessus pour plus d'informations
    echo.
    pause
    exit /b 1
)

echo.
echo 👋 Application fermée normalement
pause