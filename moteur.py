import yt_dlp
import os
import re
from pathlib import Path
import json


class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts_base = {
            'outtmpl': '%(title)s.%(ext)s',
            'ignoreerrors': True,
            'no_warnings': False,
            'extractaudio': False,
            'audioformat': 'mp3',
            'audioquality': '192',
            'format': 'best',
            'noplaylist': True,
        }

    def sanitize_filename(self, filename):
        """Nettoie le nom de fichier pour éviter les caractères problématiques"""
        # Supprimer les caractères interdits
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Supprimer les espaces en début/fin
        filename = filename.strip()
        # Limiter la longueur
        if len(filename) > 200:
            filename = filename[:200]
        return filename

    def get_video_info(self, url, is_playlist=False):
        """Récupère les informations d'une vidéo ou playlist YouTube"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'playliststart': 1,
                'playlistend': 5 if is_playlist else 1,  # Limiter pour l'aperçu
            }

            if not is_playlist:
                ydl_opts['noplaylist'] = True

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if not info:
                    return None

                # Si c'est une playlist
                if is_playlist and 'entries' in info:
                    first_video = None
                    for entry in info['entries']:
                        if entry:
                            first_video = entry
                            break

                    if first_video:
                        result = {
                            'title': first_video.get('title', 'Titre non disponible'),
                            'uploader': first_video.get('uploader', 'Auteur non disponible'),
                            'duration_string': self.format_duration(first_video.get('duration', 0)),
                            'view_count': first_video.get('view_count', 0),
                            'playlist_title': info.get('title', 'Playlist sans titre'),
                            'playlist_count': info.get('playlist_count', len([e for e in info['entries'] if e])),
                            'formats': self.get_available_formats(first_video)
                        }
                    else:
                        return None
                else:
                    # Vidéo simple
                    result = {
                        'title': info.get('title', 'Titre non disponible'),
                        'uploader': info.get('uploader', 'Auteur non disponible'),
                        'duration_string': self.format_duration(info.get('duration', 0)),
                        'view_count': info.get('view_count', 0),
                        'formats': self.get_available_formats(info)
                    }

                return result

        except Exception as e:
            print(f"Erreur lors de l'extraction des informations: {e}")
            return None

    def format_duration(self, seconds):
        """Formate la durée en format lisible"""
        if not seconds:
            return "Durée inconnue"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def get_available_formats(self, info):
        """Récupère les formats disponibles"""
        formats = []
        if 'formats' in info:
            seen_qualities = set()
            for f in info['formats']:
                if f.get('height') and f.get('ext'):
                    quality = f"{f['height']}p"
                    if quality not in seen_qualities:
                        formats.append(f"{quality} ({f['ext']})")
                        seen_qualities.add(quality)

        return formats[:10]  # Limiter à 10 formats

    def get_format_selector(self, quality, format_type):
        """Retourne le sélecteur de format pour yt-dlp"""

        # Formats audio uniquement
        if format_type in ['mp3', 'm4a']:
            if format_type == 'mp3':
                return 'bestaudio[ext=m4a]/bestaudio/best'
            else:
                return 'bestaudio[ext=m4a]/bestaudio'

        # Formats vidéo
        if quality == 'best':
            return f'best[ext={format_type}]/best'

        # Qualité spécifique
        height = quality.replace('p', '')

        format_selectors = [
            f'best[height<={height}][ext={format_type}]',
            f'best[height<={height}]',
            f'bestvideo[height<={height}]+bestaudio/best[height<={height}]',
            'best'
        ]

        return '/'.join(format_selectors)

    def download(self, url, output_path, quality='720p', format_type='mp4', is_playlist=False, progress_callback=None):
        """Télécharge une vidéo ou playlist YouTube"""
        try:
            # Créer le dossier de sortie
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)

            # Configuration yt-dlp
            ydl_opts = self.ydl_opts_base.copy()

            # Chemin de sortie
            if is_playlist:
                ydl_opts['outtmpl'] = str(output_path / '%(playlist_title)s/%(title)s.%(ext)s')
                ydl_opts['noplaylist'] = False
            else:
                ydl_opts['outtmpl'] = str(output_path / '%(title)s.%(ext)s')
                ydl_opts['noplaylist'] = True

            # Format
            ydl_opts['format'] = self.get_format_selector(quality, format_type)

            # Configuration audio pour MP3
            if format_type == 'mp3':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            elif format_type == 'm4a':
                ydl_opts.update({
                    'format': 'bestaudio[ext=m4a]/bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                        'preferredquality': '192',
                    }],
                })

            # Callback de progression
            if progress_callback:
                ydl_opts['progress_hooks'] = [progress_callback]

            # Téléchargement
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return True

        except Exception as e:
            print(f"Erreur lors du téléchargement: {e}")
            return False

    def get_playlist_info(self, url):
        """Récupère les informations détaillées d'une playlist"""
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'playliststart': 1,
                'playlistend': 100,  # Limiter pour éviter les très grosses playlists
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if 'entries' in info:
                    videos = []
                    for entry in info['entries']:
                        if entry:
                            videos.append({
                                'title': entry.get('title', 'Titre non disponible'),
                                'url': entry.get('url', ''),
                                'duration': self.format_duration(entry.get('duration', 0))
                            })

                    return {
                        'playlist_title': info.get('title', 'Playlist sans titre'),
                        'playlist_count': len(videos),
                        'videos': videos
                    }

                return None

        except Exception as e:
            print(f"Erreur lors de l'extraction de la playlist: {e}")
            return None

    def is_valid_url(self, url):
        """Vérifie si l'URL est une URL YouTube valide"""
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        return re.match(youtube_regex, url) is not None

    def extract_video_id(self, url):
        """Extrait l'ID de la vidéo depuis l'URL"""
        youtube_regex = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&=%\?]{11})'
        match = re.search(youtube_regex, url)
        return match.group(1) if match else None

    def get_thumbnail_url(self, video_id):
        """Retourne l'URL de la miniature de la vidéo"""
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    def check_ffmpeg(self):
        """Vérifie si FFmpeg est disponible"""
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'],
                                    capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False