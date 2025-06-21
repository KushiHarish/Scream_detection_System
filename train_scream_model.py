import os
import numpy as np
from utils.audio_features import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Paths (corrected folder names)
scream_path = "dataset/Screaming"  # Screaming folder
non_scream_path = "dataset/NotScreaming"  # NotScreaming folder

X = []
y = []

# Load scream files
print("Loading scream files...")
for filename in os.listdir(scream_path):
    file_path = os.path.join(scream_path, filename)
    features = extract_features(file_path)
    if features is not None:
        X.append(features)
        y.append(1)  # 1 = Scream

# Load non-scream files
print("Loading non-scream files...")
for filename in os.listdir(non_scream_path):
    file_path = os.path.join(non_scream_path, filename)
    features = extract_features(file_path)
    if features is not None:
        X.append(features)
        y.append(0)  # 0 = Non-scream

print("Total files processed:", len(X))

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

# Train-test split
print("Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("Training the RandomForest model...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
print("Saving the model...")
joblib.dump(clf, "models/scream_detector.pkl")
print("✅ Model saved as models/scream_detector.pkl")
