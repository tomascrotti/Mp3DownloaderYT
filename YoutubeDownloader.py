import tkinter as tk
from tkinter import messagebox, filedialog
import os
import yt_dlp

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Youtube MP3 Downloader")

        # Etiqueta y campo de entrada de URL
        self.label_url = tk.Label(self, text="Ingrese la URL del video:")
        self.label_url.pack(pady=10)
        
        self.entrada_url = tk.Entry(self, width=50)
        self.entrada_url.pack(pady=10)
        self.entrada_url.bind("<KeyRelease>", self.update_nombre_video)

        # Etiqueta para mostrar el nombre del video
        self.label_nombre = tk.Label(self, text="")
        self.label_nombre.pack(pady=5)
        
        # Botones de descargar y cancelar
        self.btn_download = tk.Button(self, text="Descargar MP3", state=tk.DISABLED, command=self.download_mp3)
        self.btn_download.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.btn_cancel = tk.Button(self, text="Cancelar", command=self.quit)
        self.btn_cancel.pack(side=tk.RIGHT, padx=20, pady=20)

        # Botón directorio
        self.btn_path = tk.Button(self, text="Carpeta...", command=self.carpeta)
        self.btn_path.pack(side=tk.RIGHT, padx=20, pady=20)

    def carpeta(self):
        self.directorio = filedialog.askdirectory(initialdir=r"C:\Usuarios\Usuario", title="Seleccione la carpeta")
        if not self.directorio:
            self.directorio = "."

    def centrar_ventana(self, ancho=400, alto=200):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = int((pantalla_ancho/2) - (self.ancho/2))
        y = int((pantalla_alto/2) - (self.alto/2))
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def update_nombre_video(self, event=None):
        url = self.entrada_url.get()
        if not url:
            self.label_nombre.config(text="")
            self.btn_download.config(state=tk.DISABLED)
            return
        
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_nombre = info_dict.get('title', None)
                self.label_nombre.config(text=video_nombre)
                self.btn_download.config(state=tk.NORMAL)
        except Exception as e:
            self.label_nombre.config(text=f"Error: {str(e)}")
            self.btn_download.config(state=tk.DISABLED)

    def download_mp3(self):
        url = self.entrada_url.get()
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self.directorio, '%(title)s.%(ext)s'),
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("Éxito", "Descarga completa")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar el video. Detalles: {e}")

if __name__ == '__main__':
    app = YouTubeDownloader()
    app.mainloop()
    app.centrar_ventana(400,200)