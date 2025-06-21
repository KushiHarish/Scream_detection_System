import librosa
import numpy as np

def extract_features(file_path):
    try:
        # Load audio in mono at 16kHz
        y, sr = librosa.load(file_path, sr=16000, mono=True)

        # Extract audio features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

        # Combine all features into one vector
        feature_vector = np.hstack([
            np.mean(mfcc, axis=1),
            np.mean(chroma, axis=1),
            np.mean(contrast, axis=1)
        ])

        return feature_vector

    except Exception as e:
        print(f"[ERROR] Could not process {file_path}: {e}")
        return None
