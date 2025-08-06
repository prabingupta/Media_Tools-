

# video_editor_gui.py
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from video_editor import enhance_video

def start_enhancement():
    input_path = filedialog.askopenfilename(
        title="Select Input Video",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv")]
    )
    if not input_path:
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        title="Save Enhanced Video As",
        filetypes=[("MP4 Files", "*.mp4")]
    )
    if not output_path:
        return

    thread = threading.Thread(target=run_enhancement, args=(input_path, output_path))
    thread.start()

def run_enhancement(input_path, output_path):
    try:
        progress_label.config(text="Enhancement in progress...")
        progress_bar['value'] = 0
        root.update_idletasks()

        enhance_video(input_path, output_path, progress_callback=update_progress)

        messagebox.showinfo("Success ✅", f"Enhanced video saved to:\n{output_path}")
        progress_label.config(text="Done ✅")
    except Exception as e:
        messagebox.showerror("Error ❌", str(e))
        progress_label.config(text="Failed ❌")

def update_progress(percent):
    progress_bar['value'] = percent
    progress_label.config(text=f"Enhancing... {percent}%")
    root.update_idletasks()

# GUI setup
root = tk.Tk()
root.title("4K Video Enhancer")

# Set window size and icon (optional)
root.geometry("460x360")
try:
    root.iconbitmap("icon.ico")  # For Windows (.ico only). Skip or replace if not available.
except:
    pass

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

# Optional logo (requires 'logo.png' in same directory)
if os.path.exists("logo.png"):
    logo_img = Image.open("logo.png").resize((100, 100))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame, image=logo_photo)
    logo_label.image = logo_photo
    logo_label.pack(pady=(0, 10))

# Title
title = tk.Label(frame, text="4K Video Enhancer using RealESRGAN", font=("Helvetica", 14, "bold"))
title.pack(pady=10)

# Enhance Button
enhance_button = tk.Button(
    frame,
    text="Select Video to Enhance",
    command=start_enhancement,
    height=2,
    width=25,
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 12)
)
enhance_button.pack(pady=10)

# Progress Bar and Label
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=(10, 5))

progress_label = tk.Label(frame, text="", font=("Helvetica", 12))
progress_label.pack(pady=5)

root.mainloop()
