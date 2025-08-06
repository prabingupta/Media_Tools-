# test_gui.py
import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry("300x150")
tk.Label(root, text="✅ Tkinter is working!").pack(pady=30)
root.mainloop()
