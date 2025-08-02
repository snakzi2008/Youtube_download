#!/usr/bin/env python3
"""
YouTube Downloader Pro - Script de démarrage
Ce script vérifie les dépendances et lance l'application
"""

import sys
import os
import subprocess
import importlib.util


def check_dependency(module_name, install_name=None):
    """Vérifie si un module est installé"""
    if install_name is None:
        install_name = module_name

    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ Module {module_name} non trouvé")
        return False
    return True


def install_missing_dependencies():
    """Installe automatiquement les dépendances manquantes"""
    print("🔧 Installation des dépendances manquantes...")

    dependencies = {
        'customtkinter': 'customtkinter==5.2.2',
        'yt_dlp': 'yt-dlp==2024.1.7',
        'PIL': 'Pillow==10.2.0',
        'requests': 'requests==2.31.0'
    }

    missing_deps = []
    for module, package in dependencies.items():
        if not check_dependency(module):
            missing_deps.append(package)

    if missing_deps:
        print(f"📦 Installation de {len(missing_deps)} dépendance(s)...")
        for package in missing_deps:
            try:
                print(f"⏳ Installation de {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package,
                    "--upgrade", "--user"
                ])
                print(f"✅ {package} installé")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur lors de l'installation de {package}: {e}")
                return False

        print("✅ Toutes les dépendances ont été installées!")
        return True
    else:
        print("✅ Toutes les dépendances sont déjà installées")
        return True


def check_python_version():
    """Vérifie la version de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ requis. Version actuelle: {version.major}.{version.minor}")
        return False
    return True


def create_folders():
    """Crée les dossiers nécessaires"""
    folders = ['telechargements', 'temp']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def main():
    """Fonction principale"""
    print("🎥 YouTube Downloader Pro")
    print("=" * 40)

    # Vérifier Python
    if not check_python_version():
        input("Appuyez sur Entrée pour quitter...")
        return 1

    # Créer les dossiers
    create_folders()

    # Vérifier et installer les dépendances
    if not install_missing_dependencies():
        print("❌ Impossible d'installer les dépendances requises")
        print("💡 Essayez de lancer setup.py d'abord")
        input("Appuyez sur Entrée pour quitter...")
        return 1

    # Importer et lancer l'application
    try:
        print("🚀 Lancement de l'application...")

        # Ajouter le répertoire courant au path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Importer l'interface
        from interface import YouTubeDownloaderGUI

        # Créer et lancer l'application
        app = YouTubeDownloaderGUI()
        print("✅ Application lancée avec succès!")
        app.run()

    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("💡 Vérifiez que tous les fichiers sont présents:")
        print("   - interface.py")
        print("   - moteur.py")
        print("   - start.py")
        input("Appuyez sur Entrée pour quitter...")
        return 1

    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()
        input("Appuyez sur Entrée pour quitter...")
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)