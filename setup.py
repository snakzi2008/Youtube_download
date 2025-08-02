import os
import sys
import subprocess
import platform


def install_requirements():
    """Installe les dépendances requises"""
    print("🔧 Installation des dépendances...")

    requirements = [
        "customtkinter==5.2.2",
        "yt-dlp==2024.1.7",
        "Pillow==10.2.0",
        "requests==2.31.0",
        "urllib3==2.1.0"
    ]

    for requirement in requirements:
        try:
            print(f"📦 Installation de {requirement}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"✅ {requirement} installé avec succès")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation de {requirement}: {e}")
            return False

    print("✅ Toutes les dépendances ont été installées avec succès!")
    return True


def check_python_version():
    """Vérifie que la version de Python est compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou supérieur est requis")
        print(f"Version actuelle: {version.major}.{version.minor}.{version.micro}")
        return False

    print(f"✅ Version Python compatible: {version.major}.{version.minor}.{version.micro}")
    return True


def create_directories():
    """Crée les dossiers nécessaires"""
    print("📁 Création des dossiers...")

    directories = [
        "telechargements",
        "temp"
    ]

    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Dossier '{directory}' créé")
        except Exception as e:
            print(f"❌ Erreur lors de la création du dossier '{directory}': {e}")
            return False

    return True


def check_ffmpeg():
    """Vérifie et installe FFmpeg si nécessaire"""
    print("🎬 Vérification de FFmpeg...")

    try:
        subprocess.run(['ffmpeg', '-version'],
                       capture_output=True, check=True, timeout=5)
        print("✅ FFmpeg est disponible")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("⚠️  FFmpeg n'est pas installé")
        print("🔧 Installation automatique de FFmpeg...")

        system = platform.system().lower()

        if system == "windows":
            print("Windows détecté - Installation via winget...")
            try:
                subprocess.run(['winget', 'install', 'ffmpeg'], check=True)
                print("✅ FFmpeg installé via winget")
                return True
            except:
                print("❌ Échec de l'installation automatique")
                print("📝 Veuillez installer FFmpeg manuellement:")
                print("   1. Téléchargez FFmpeg depuis https://ffmpeg.org/download.html")
                print("   2. Ajoutez FFmpeg au PATH système")
                return False

        elif system == "darwin":  # macOS
            print("macOS détecté - Installation via Homebrew...")
            try:
                subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
                print("✅ FFmpeg installé via Homebrew")
                return True
            except:
                print("❌ Échec de l'installation automatique")
                print("📝 Veuillez installer FFmpeg manuellement:")
                print("   brew install ffmpeg")
                return False

        else:  # Linux
            print("Linux détecté - Installation via gestionnaire de paquets...")
            try:
                # Essayer apt (Ubuntu/Debian)
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)
                print("✅ FFmpeg installé via apt")
                return True
            except:
                try:
                    # Essayer yum (CentOS/RHEL)
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'ffmpeg'], check=True)
                    print("✅ FFmpeg installé via yum")
                    return True
                except:
                    try:
                        # Essayer pacman (Arch)
                        subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], check=True)
                        print("✅ FFmpeg installé via pacman")
                        return True
                    except:
                        print("❌ Échec de l'installation automatique")
                        print("📝 Veuillez installer FFmpeg manuellement:")
                        print("   sudo apt install ffmpeg  # Ubuntu/Debian")
                        print("   sudo yum install ffmpeg  # CentOS/RHEL")
                        print("   sudo pacman -S ffmpeg   # Arch Linux")
                        return False


def main():
    """Fonction principale de configuration"""
    print("🚀 Configuration de YouTube Downloader Pro")
    print("=" * 50)

    # Vérifier la version Python
    if not check_python_version():
        input("Appuyez sur Entrée pour quitter...")
        return

    # Créer les dossiers
    if not create_directories():
        print("❌ Erreur lors de la création des dossiers")
        input("Appuyez sur Entrée pour quitter...")
        return

    # Installer les dépendances
    if not install_requirements():
        print("❌ Erreur lors de l'installation des dépendances")
        input("Appuyez sur Entrée pour quitter...")
        return

    # Vérifier FFmpeg
    ffmpeg_ok = check_ffmpeg()
    if not ffmpeg_ok:
        print("⚠️  L'application fonctionnera mais sans conversion audio")

    print("\n" + "=" * 50)
    print("🎉 Configuration terminée avec succès!")
    print("▶️  Vous pouvez maintenant lancer l'application avec start.py")

    if not ffmpeg_ok:
        print("⚠️  Note: FFmpeg n'est pas installé - certaines fonctionnalités seront limitées")

    input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()