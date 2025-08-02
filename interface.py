import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from moteur import YouTubeDownloader
import webbrowser


class YouTubeDownloaderGUI:
    def __init__(self):
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Variables
        self.download_path = tk.StringVar(value=os.path.join(os.getcwd(), "telechargements"))
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="720p")
        self.format_var = tk.StringVar(value="mp4")
        self.playlist_var = tk.BooleanVar()

        # Créer le dossier de téléchargement s'il n'existe pas
        os.makedirs(self.download_path.get(), exist_ok=True)

        # Initialiser le moteur de téléchargement
        self.downloader = YouTubeDownloader()

        # Créer l'interface
        self.create_widgets()

    def create_widgets(self):
        # Frame principal avec scrollbar
        main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎥 YouTube Downloader Pro",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(0, 30))

        # Section URL
        url_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        url_frame.pack(fill="x", pady=(0, 20))

        url_title = ctk.CTkLabel(
            url_frame,
            text="📎 URL de la vidéo ou playlist",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        url_title.pack(pady=(20, 10))

        self.url_entry = ctk.CTkEntry(
            url_frame,
            textvariable=self.url_var,
            placeholder_text="Collez l'URL YouTube ici...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.url_entry.pack(fill="x", padx=20, pady=(0, 10))

        # Bouton pour coller depuis le presse-papiers
        paste_btn = ctk.CTkButton(
            url_frame,
            text="📋 Coller",
            command=self.paste_url,
            height=35,
            width=100
        )
        paste_btn.pack(pady=(0, 20))

        # Section Options
        options_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        options_frame.pack(fill="x", pady=(0, 20))

        options_title = ctk.CTkLabel(
            options_frame,
            text="⚙️ Options de téléchargement",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        options_title.pack(pady=(20, 20))

        # Grille pour les options
        options_grid = ctk.CTkFrame(options_frame, fg_color="transparent")
        options_grid.pack(fill="x", padx=20)

        # Qualité
        quality_label = ctk.CTkLabel(options_grid, text="Qualité:", font=ctk.CTkFont(size=14))
        quality_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)

        quality_menu = ctk.CTkOptionMenu(
            options_grid,
            variable=self.quality_var,
            values=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "best"],
            width=120
        )
        quality_menu.grid(row=0, column=1, sticky="w", pady=10)

        # Format
        format_label = ctk.CTkLabel(options_grid, text="Format:", font=ctk.CTkFont(size=14))
        format_label.grid(row=0, column=2, sticky="w", padx=(20, 10), pady=10)

        format_menu = ctk.CTkOptionMenu(
            options_grid,
            variable=self.format_var,
            values=["mp4", "webm", "mp3", "m4a"],
            width=100
        )
        format_menu.grid(row=0, column=3, sticky="w", pady=10)

        # Checkbox playlist
        playlist_check = ctk.CTkCheckBox(
            options_grid,
            text="Télécharger toute la playlist",
            variable=self.playlist_var,
            font=ctk.CTkFont(size=14)
        )
        playlist_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=10)

        # Section Dossier de destination
        path_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        path_frame.pack(fill="x", pady=(0, 20))

        path_title = ctk.CTkLabel(
            path_frame,
            text="📁 Dossier de destination",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        path_title.pack(pady=(20, 10))

        path_container = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_container.pack(fill="x", padx=20)

        self.path_entry = ctk.CTkEntry(
            path_container,
            textvariable=self.download_path,
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            path_container,
            text="📂 Parcourir",
            command=self.browse_folder,
            height=40,
            width=120
        )
        browse_btn.pack(side="right", pady=(0, 20))

        path_frame.pack_configure(pady=(0, 20))

        # Boutons d'action
        action_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        action_frame.pack(fill="x", pady=(0, 20))

        buttons_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        buttons_container.pack(pady=20)

        # Bouton Analyser
        self.analyze_btn = ctk.CTkButton(
            buttons_container,
            text="🔍 Analyser la vidéo",
            command=self.analyze_video,
            height=50,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.analyze_btn.pack(side="left", padx=10)

        # Bouton Télécharger
        self.download_btn = ctk.CTkButton(
            buttons_container,
            text="⬇️ Télécharger",
            command=self.start_download,
            height=50,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2b8a3e",
            hover_color="#37a24b"
        )
        self.download_btn.pack(side="left", padx=10)

        # Section Informations
        self.info_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        self.info_frame.pack(fill="x", pady=(0, 20))

        info_title = ctk.CTkLabel(
            self.info_frame,
            text="ℹ️ Informations",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        info_title.pack(pady=(20, 10))

        self.info_text = ctk.CTkTextbox(
            self.info_frame,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.info_text.pack(fill="x", padx=20, pady=(0, 20))

        # Barre de progression
        self.progress_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        self.progress_frame.pack(fill="x", pady=(0, 20))

        progress_title = ctk.CTkLabel(
            self.progress_frame,
            text="📊 Progression",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        progress_title.pack(pady=(20, 10))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=20)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Prêt à télécharger",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=(0, 20))

        # Footer
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(20, 0))

        footer_label = ctk.CTkLabel(
            footer_frame,
            text="Développé avec ❤️ - YouTube Downloader Pro v1.0",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        footer_label.pack()

    def paste_url(self):
        """Colle l'URL depuis le presse-papiers"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_var.set(clipboard_content)
        except:
            pass

    def browse_folder(self):
        """Ouvre le dialogue pour choisir le dossier de destination"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)

    def update_info(self, text):
        """Met à jour le texte d'information"""
        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", text)

    def update_progress(self, value, text=""):
        """Met à jour la barre de progression"""
        self.progress_bar.set(value)
        if text:
            self.progress_label.configure(text=text)
        self.root.update_idletasks()

    def analyze_video(self):
        """Analyse la vidéo/playlist YouTube"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube valide")
            return

        def analyze_thread():
            try:
                self.analyze_btn.configure(state="disabled", text="🔄 Analyse...")
                self.update_info("Analyse de la vidéo en cours...\n")

                info = self.downloader.get_video_info(url, self.playlist_var.get())

                if info:
                    info_text = f"✅ Analyse terminée !\n\n"
                    if self.playlist_var.get() and 'playlist_count' in info:
                        info_text += f"📋 Playlist: {info.get('playlist_title', 'Sans titre')}\n"
                        info_text += f"📊 Nombre de vidéos: {info['playlist_count']}\n\n"
                        info_text += f"🎬 Première vidéo: {info.get('title', 'Titre non disponible')}\n"
                    else:
                        info_text += f"🎬 Titre: {info.get('title', 'Titre non disponible')}\n"

                    info_text += f"👤 Auteur: {info.get('uploader', 'Auteur non disponible')}\n"
                    info_text += f"⏱️ Durée: {info.get('duration_string', 'Durée non disponible')}\n"
                    info_text += f"👀 Vues: {info.get('view_count', 'Vues non disponibles'):,}\n"

                    if 'formats' in info:
                        info_text += f"\n📺 Formats disponibles:\n"
                        for fmt in info['formats'][:5]:  # Afficher les 5 premiers formats
                            info_text += f"  • {fmt}\n"

                    self.update_info(info_text)
                else:
                    self.update_info("❌ Impossible d'analyser cette URL.\nVérifiez que l'URL est valide et accessible.")

            except Exception as e:
                self.update_info(f"❌ Erreur lors de l'analyse:\n{str(e)}")
            finally:
                self.analyze_btn.configure(state="normal", text="🔍 Analyser la vidéo")

        threading.Thread(target=analyze_thread, daemon=True).start()

    def start_download(self):
        """Démarre le téléchargement"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube valide")
            return

        # Créer le dossier s'il n'existe pas
        download_dir = self.download_path.get()
        os.makedirs(download_dir, exist_ok=True)

        def download_thread():
            try:
                self.download_btn.configure(state="disabled", text="🔄 Téléchargement...")
                self.update_progress(0, "Initialisation du téléchargement...")

                # Callback pour la progression
                def progress_callback(d):
                    if d['status'] == 'downloading':
                        if 'total_bytes' in d and d['total_bytes']:
                            percent = d['downloaded_bytes'] / d['total_bytes']
                            self.update_progress(percent, f"Téléchargement: {percent * 100:.1f}%")
                        else:
                            self.update_progress(0.5, "Téléchargement en cours...")
                    elif d['status'] == 'finished':
                        self.update_progress(1.0, "Téléchargement terminé !")

                # Télécharger
                success = self.downloader.download(
                    url=url,
                    output_path=download_dir,
                    quality=self.quality_var.get(),
                    format_type=self.format_var.get(),
                    is_playlist=self.playlist_var.get(),
                    progress_callback=progress_callback
                )

                if success:
                    self.update_info(
                        f"✅ Téléchargement terminé avec succès !\n\nFichiers sauvegardés dans:\n{download_dir}")
                    messagebox.showinfo("Succès", "Téléchargement terminé avec succès !")

                    # Proposer d'ouvrir le dossier
                    if messagebox.askyesno("Ouvrir le dossier", "Voulez-vous ouvrir le dossier de téléchargement ?"):
                        os.startfile(download_dir) if os.name == 'nt' else os.system(f'open "{download_dir}"')
                else:
                    self.update_info("❌ Échec du téléchargement.\nVérifiez l'URL et votre connexion internet.")
                    messagebox.showerror("Erreur", "Échec du téléchargement")

            except Exception as e:
                error_msg = f"❌ Erreur lors du téléchargement:\n{str(e)}"
                self.update_info(error_msg)
                messagebox.showerror("Erreur", f"Erreur lors du téléchargement:\n{str(e)}")
            finally:
                self.download_btn.configure(state="normal", text="⬇️ Télécharger")
                self.update_progress(0, "Prêt à télécharger")

        threading.Thread(target=download_thread, daemon=True).start()

    def run(self):
        """Lance l'application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = YouTubeDownloaderGUI()
    app.run()