import tkinter as tk
from tkinter import messagebox
import yt_dlp

# Define resolution format mapping
resolution_formats = {
    '4K': 'bestvideo[height=2160]+bestaudio/best',
    '1080p': 'bestvideo[height=1080]+bestaudio/best',
    '720p': 'bestvideo[height=720]+bestaudio/best'
}

def download_video():
    video_url = url_entry.get().strip()
    resolution = resolution_var.get()

    if not video_url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    selected_format = resolution_formats.get(resolution, 'best')

    ydl_opts = {
        'format': selected_format,
        'merge_output_format': 'mp4',
        'outtmpl': '/Users/prabinkumargupta/Downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            status_label.config(text="Downloading...")
            ydl.download([video_url])
            status_label.config(text="Download completed!")
            messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="Download failed.")

# Create main window
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("450x250")
root.resizable(False, False)

# URL input
tk.Label(root, text="YouTube Video URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=50, font=("Arial", 11))
url_entry.pack()

# Resolution selection
tk.Label(root, text="Select Resolution:", font=("Arial", 12)).pack(pady=10)
resolution_var = tk.StringVar(value="1080p")
res_options = ["4K", "1080p", "720p"]
resolution_menu = tk.OptionMenu(root, resolution_var, *res_options)
resolution_menu.pack()

# Download button
download_button = tk.Button(root, text="Download", font=("Arial", 12, "bold"), command=download_video)
download_button.pack(pady=15)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 10), fg="green")
status_label.pack()

# Run GUI
root.mainloop()
