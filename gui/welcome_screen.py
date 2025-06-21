import tkinter as tk
from tkinter import PhotoImage
import os
import sys

def show_welcome():
    root = tk.Tk()
    root.title("Welcome - ScreamGuard")

    # Fixed size window, centered
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#151515")
    root.resizable(False, False)

    # Load and place image
    try:
        image_path = os.path.join("gui", "welcome_background.png")
        image = PhotoImage(file=image_path)
    except Exception as e:
        print(f"Image load failed: {e}")
        root.destroy()
        return

    img_label = tk.Label(root, image=image, bg="#151515")
    img_label.pack(pady=(40, 20))  # top margin, bottom margin

    # Text under image
    title = tk.Label(root, text="👋 Welcome to ScreamGuard", font=("Helvetica", 16, "bold"), fg="white", bg="#151515")
    title.pack()

    subtitle = tk.Label(root, text="Smart Scream Detection System", font=("Helvetica", 12), fg="gray", bg="#151515")
    subtitle.pack()

    # Keep a reference to avoid garbage collection
    root.image = image

    # Launch main UI after 3 seconds
    root.after(3000, lambda: go_to_main(root))
    root.mainloop()

def go_to_main(splash_window):
    splash_window.destroy()
    splash_window.quit()
    
    # Run main_interface.py as a separate process
    main_module_path = os.path.join("gui", "main_interface.py")
    #subprocess.Popen([sys.executable, main_module_path])

if __name__ == "__main__":
    print("Launching splash screen...")
    show_welcome()
