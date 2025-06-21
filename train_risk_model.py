import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from utils.audio_features import extract_features

# Paths to the risk categories
safe_path = "dataset/RiskLevels/Safe"
medium_path = "dataset/RiskLevels/Medium"
high_path = "dataset/RiskLevels/High"

X = []
y = []

# Load Safe files
print("Loading Safe files...")
for filename in os.listdir(safe_path):
    file_path = os.path.join(safe_path, filename)
    features = extract_features(file_path)
    if features is not None:
        X.append(features)
        y.append(0)  # 0 = Safe

# Load Medium files
print("Loading Medium files...")
for filename in os.listdir(medium_path):
    file_path = os.path.join(medium_path, filename)
    features = extract_features(file_path)
    if features is not None:
        X.append(features)
        y.append(1)  # 1 = Medium

# Load High files
print("Loading High files...")
for filename in os.listdir(high_path):
    file_path = os.path.join(high_path, filename)
    features = extract_features(file_path)
    if features is not None:
        X.append(features)
        y.append(2)  # 2 = High

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
print("Saving the risk model...")
joblib.dump(clf, "models/risk_classifier.pkl")
print("✅ Risk model saved as models/risk_classifier.pkl")
