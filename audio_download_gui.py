import tkinter as tk
from tkinter import messagebox
from audio_download import download_audio

def download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    status = download_audio(url)
    if status.startswith("Downloaded"):
        messagebox.showinfo("Success", status)
    else:
        messagebox.showerror("Failed", status)

# GUI setup
root = tk.Tk()
root.title("YouTube Audio Downloader")

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_btn = tk.Button(root, text="Download MP3", command=download)
download_btn.pack(pady=10)

root.mainloop()

