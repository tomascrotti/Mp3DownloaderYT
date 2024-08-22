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

if __name__ == '__main__':
    app = YouTubeDownloader()
    app.mainloop()