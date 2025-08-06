import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
from photo_editor import enhance_photo

def start_enhancement():
    input_path = filedialog.askopenfilename(
        title="Select Photo",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not input_path:
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        title="Save Enhanced Photo As",
        filetypes=[("PNG Files", "*.png")]
    )
    if not output_path:
        return

    def run_enhancement():
        try:
            print("[GUI] Enhancement started")
            enhance_button.config(state=tk.DISABLED)
            progress_bar.start(10)
            status_label.config(text="Enhancement in progress...")
            
            enhance_photo(input_path, output_path)
            
            progress_bar.stop()
            status_label.config(text="Done ✅")
            messagebox.showinfo("Success ✅", f"Enhanced photo saved to:\n{output_path}")
            print("[GUI] Enhancement finished successfully")
        except Exception as e:
            progress_bar.stop()
            status_label.config(text="Failed ❌")
            print(f"[GUI ERROR] {e}")
            messagebox.showerror("Error ❌", str(e))
        finally:
            enhance_button.config(state=tk.NORMAL)

    threading.Thread(target=run_enhancement, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("4K Photo Enhancer")
root.geometry("400x220")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

title_label = tk.Label(frame, text="4K Photo Enhancer using RealESRGAN", font=("Helvetica", 14))
title_label.pack(pady=10)

enhance_button = tk.Button(frame, text="Select Photo to Enhance", command=start_enhancement, height=2, width=25)
enhance_button.pack(pady=10)

progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="indeterminate", length=250)
progress_bar.pack(pady=10)

status_label = tk.Label(frame, text="", font=("Helvetica", 12))
status_label.pack()

root.mainloop()
