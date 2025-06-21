# utils/audio_utils.py
import matplotlib.pyplot as plt
import librosa
import librosa.display
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_waveform(audio_path, canvas_frame):
    try:
        y, sr = librosa.load(audio_path, sr=16000)
        
        # Create a figure and axis for the waveform
        fig, ax = plt.subplots(figsize=(6, 2), dpi=100)
        librosa.display.waveshow(y, sr=sr, color='cyan', ax=ax)
        ax.set_title('Waveform')

        # Remove any existing widgets in the canvas_frame (clear previous canvas)
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        # Create a canvas from the figure and display it in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)  # Embed the figure into Tkinter frame
        canvas.draw()  # Draw the figure on the canvas
        canvas.get_tk_widget().pack()  # Display the canvas in Tkinter window

    except Exception as e:
        print(f"[Waveform Error] {e}")
