import sys
import librosa
import librosa.display
import matplotlib
matplotlib.use('qtagg')  # Qt backend for PyQt6

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QFrame, QSplashScreen
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

import pygame
pygame.mixer.init()

from utils import mic_recorder  # your own module
import predict  # your own module

class ScreamGuardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScreamGuard - Detection Panel")
        self.setGeometry(100, 100, 900, 600)

        self.uploaded_audio_path = None
        self.recorded_audio_path = None

        self.init_ui()

    def init_ui(self):
        font_btn = QFont("Arial", 12)

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.title_label = QLabel("🎤 Smart Scream Detection")
        self.title_label.setFont(QFont("Helvetica", 20, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

        self.upload_btn = QPushButton("📁 Upload Audio")
        self.upload_btn.setFont(font_btn)
        self.upload_btn.clicked.connect(self.upload_audio)

        self.record_btn = QPushButton("🎙️ Record Audio")
        self.record_btn.setFont(font_btn)
        self.record_btn.clicked.connect(self.record_audio)

        self.play_btn = QPushButton("🔊 Play Audio")
        self.play_btn.setFont(font_btn)
        self.play_btn.clicked.connect(self.play_audio)

        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.setFont(font_btn)
        self.reset_btn.clicked.connect(self.reset_result)

        for btn in [self.upload_btn, self.record_btn, self.play_btn, self.reset_btn]:
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        self.result_label = QLabel("Awaiting input...")
        self.result_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.result_label)

        self.audio_info = QLabel("")
        self.audio_info.setFont(QFont("Arial", 12))
        self.audio_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.audio_info)

        self.waveform_frame = QFrame()
        self.waveform_layout = QVBoxLayout()
        self.waveform_frame.setLayout(self.waveform_layout)
        main_layout.addWidget(self.waveform_frame)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def upload_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an audio file", "", "WAV files (*.wav)")
        if file_path:
            self.uploaded_audio_path = file_path
            self.recorded_audio_path = None
            result = predict.predict_scream(file_path)
            self.update_result_label(result)
            self.show_waveform(file_path)
            self.update_audio_info(file_path)

    def record_audio(self):
        self.result_label.setText("🎙️ Recording...")
        QApplication.processEvents()
        path = mic_recorder.record_audio()
        if path:
            self.recorded_audio_path = path
            self.uploaded_audio_path = None
            result = predict.predict_scream(path)
            self.update_result_label(result)
            self.show_waveform(path)
            self.update_audio_info(path)
        else:
            QMessageBox.critical(self, "Recording Error", "Something went wrong during recording.")

    def play_audio(self):
        audio_path = self.uploaded_audio_path or self.recorded_audio_path
        if not audio_path:
            QMessageBox.warning(self, "No Audio", "Please upload or record audio first.")
            return

        try:
            self.result_label.setText("🎧 Playing...")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        except Exception as e:
            QMessageBox.critical(self, "Playback Error", f"Error playing audio:\n{e}")
        finally:
            self.result_label.setText("✅ Audio Ready")

    def reset_result(self):
        self.uploaded_audio_path = None
        self.recorded_audio_path = None
        self.result_label.setText("Awaiting input...")
        self.audio_info.setText("")
        self.clear_waveform()

    def update_result_label(self, result):
        if "high" in result.lower():
            self.result_label.setText("🚨 High Risk Detected!")
            self.result_label.setStyleSheet("color: red;")
        elif "medium" in result.lower():
            self.result_label.setText("⚠️ Medium Risk Detected")
            self.result_label.setStyleSheet("color: orange;")
        elif "safe" in result.lower() or "no scream" in result.lower():
            self.result_label.setText("✅ Safe / No Scream")
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText(result)
            self.result_label.setStyleSheet("color: white;")

    def update_audio_info(self, file_path):
        try:
            y, sr = librosa.load(file_path)
            duration = librosa.get_duration(y=y, sr=sr)
            self.audio_info.setText(f"Duration: {duration:.2f}s | Sample Rate: {sr} Hz")
        except Exception:
            self.audio_info.setText("Failed to load audio info")

    def show_waveform(self, file_path):
        self.clear_waveform()
        y, sr = librosa.load(file_path)

        fig = Figure(figsize=(6, 2))
        ax = fig.add_subplot(111)
        librosa.display.waveshow(y, sr=sr, ax=ax)
        ax.set(title="Waveform", xlabel="Time (s)", ylabel="Amplitude")

        canvas = FigureCanvas(fig)
        self.waveform_layout.addWidget(canvas)
        canvas.draw()

    def clear_waveform(self):
        while self.waveform_layout.count():
            child = self.waveform_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter

def launch_main_interface():
    app = QApplication(sys.argv)

    # Create main splash widget (fullscreen)
    splash = QWidget()
    splash.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    splash.showFullScreen()

    # Set background color (optional)
    splash.setStyleSheet("background-color: black;")

    # Create layout
    layout = QVBoxLayout(splash)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Load and resize splash image
    pixmap = QPixmap("gui/welcome_background.png")
    screen_size = app.primaryScreen().size()
    scaled_pixmap = pixmap.scaled(int(screen_size.width() * 0.4), int(screen_size.height() * 0.4),
                              Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    image_label = QLabel()
    image_label.setPixmap(scaled_pixmap)
    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(image_label)

    # Welcome text
    welcome_label = QLabel("👋 Welcome to ScreamGuard Project")
    welcome_label.setFont(QFont("Helvetica", 20, QFont.Weight.Bold))
    welcome_label.setStyleSheet("color: white;")
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(welcome_label)

    sub_label = QLabel("Smart Scream Detection System")
    sub_label.setFont(QFont("Helvetica", 14))
    sub_label.setStyleSheet("color: lightgray;")
    sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(sub_label)

    splash.show()

    # Delay then launch main window
    def show_main():
        splash.close()
        main_win = ScreamGuardApp()
        main_win.show()
        app.main_window = main_win

    QTimer.singleShot(3000, show_main)
    sys.exit(app.exec())


if __name__ == "__main__":
    launch_main_interface()
