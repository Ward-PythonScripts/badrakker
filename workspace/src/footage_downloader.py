import yt_dlp as youtube_dl
import tkinter as tk
from tkinter import filedialog
import tkinter.simpledialog as sd



root = tk.Tk()
root.withdraw()

url = sd.askstring("Which youtube URL to download?", "url:\t\t\t\t\t\t\t\t\t")
if url is None:
    print("I guess not")
    exit()
file_path = filedialog.asksaveasfilename(defaultextension=".mp4",initialdir='footage')
if file_path is None or file_path == "":
    print("I guess not")
    exit()

ydl_opts = {
    'outtmpl': file_path
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
