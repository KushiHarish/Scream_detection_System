import joblib
from utils.audio_features import extract_features

# Load the trained models
scream_model = joblib.load("models/scream_detector.pkl")
risk_model = joblib.load("models/risk_classifier.pkl")

# Function to predict if an audio file is a scream or not
def predict_scream(audio_path):
    features = extract_features(audio_path)

    if features is None:
        return "Could not process audio file."

    # Predict if it's a scream or not
    scream_prediction = scream_model.predict([features])[0]

    if scream_prediction == 1:
        # If it's a scream, predict the risk level
        risk_prediction = risk_model.predict([features])[0]

        # Map the risk prediction to human-readable labels
        risk_labels = {0: "Safe ✅", 1: "Medium Risk ⚠️", 2: "High Risk 🚨"}
        risk_result = risk_labels[risk_prediction]

        return f"Scream Detected! {risk_result}"
    else:
        return "Normal Sound ✅"
