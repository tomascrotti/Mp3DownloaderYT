import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from pydub import AudioSegment
import os

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Youtube MP3 Downloader")
        self.geometry("400x200")

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
        self.btn_download = tk.Button(self, text="Descargar MP3", command=self.download_mp3, state=tk.DISABLED)
        self.btn_download.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.btn_cancel = tk.Button(self, text="Cancelar", command=self.quit)
        self.btn_cancel.pack(side=tk.RIGHT, padx=20, pady=20)

    def update_nombre_video(self, event=None):
        url = self.entrada_url.get()
        if not url:
            self.label_nombre.config(text="")
            self.btn_download.config(state=tk.DISABLED)
            return
        
        try:
            yt = YouTube(url=url)
            self.label_nombre.config(text=yt.title)
            self.btn_download.config(state=tk.NORMAL)
        except Exception as e:
            self.label_nombre.config(text=f"Error: {str(e)}")
            self.btn_download.config(state=tk.DISABLED)

    def download_mp3(self):
        url = self.entrada_url.get()
        ruta_salida = "."
        try:
            yt = YouTube(url=url)
            audio_video = yt.streams.filter(only_audio=True).first()
            mp4 = audio_video.download(output_path=ruta_salida)
            mp3 = os.path.splitext(mp4)[0] + '.mp3'
            audio = AudioSegment.from_file(mp4)
            audio.export(mp3, format="mp3")
            os.remove(mp4)
            messagebox.showinfo("Éxito",f"Descarga completa: {mp3}")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo descargar el video. ERROR {e}")


if __name__ == '__main__':
    app = YouTubeDownloader()
    app.mainloop()