# mic_recorder.py

import sounddevice as sd
import soundfile as sf
import os
import pygame
pygame.mixer.init()

def record_audio(filename='audio/temp_audio.wav', duration=4, fs=16000):
    # Ensure the audio folder exists
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Created folder: {folder}")

    print(f"🎙️ Recording to {filename} for {duration} seconds...")

    # Record the audio
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')  
    sd.wait()  # Wait for the recording to finish

    try:
        # Save the audio as a .wav file
        sf.write(filename, audio, fs, format='WAV')  # Ensure it's saved in WAV format
        print(f"✅ Recording saved to {filename}")
    except Exception as e:
        print(f"Error while saving audio: {e}")

    return filename
