import os
import random
import shutil

# Paths
screaming_path = "dataset/Screaming"
safe_path = "dataset/RiskLevels/Safe"
medium_path = "dataset/RiskLevels/Medium"
high_path = "dataset/RiskLevels/High"

# Create directories if they don't exist
os.makedirs(safe_path, exist_ok=True)
os.makedirs(medium_path, exist_ok=True)
os.makedirs(high_path, exist_ok=True)

# Get all screaming files
screaming_files = [f for f in os.listdir(screaming_path) if f.endswith('.wav')]

# Debug: Print number of files found
print(f"Found {len(screaming_files)} .wav files in the 'Screaming' folder.")

# If no files found, exit
if len(screaming_files) == 0:
    print("No .wav files found in 'Screaming' folder. Exiting script.")
    exit()

# Shuffle the files to ensure randomness
random.shuffle(screaming_files)

# Number of files to distribute
num_files = len(screaming_files)

# Split into 3 categories: Safe, Medium, High
safe_count = int(num_files * 0.3)  # 30% for Safe
medium_count = int(num_files * 0.4)  # 40% for Medium
high_count = num_files - safe_count - medium_count  # Remaining for High

# Debug: Print the count for each category
print(f"Splitting {num_files} files into:\n- Safe: {safe_count}\n- Medium: {medium_count}\n- High: {high_count}")

# Distribute files into respective categories
safe_files = screaming_files[:safe_count]
medium_files = screaming_files[safe_count:safe_count + medium_count]
high_files = screaming_files[safe_count + medium_count:]

# Move files to the appropriate folder
def move_files(files, target_folder):
    for file in files:
        src = os.path.join(screaming_path, file)
        dst = os.path.join(target_folder, file)
        shutil.copy(src, dst)

# Move files to their folders
move_files(safe_files, safe_path)
move_files(medium_files, medium_path)
move_files(high_files, high_path)

# Debug: Confirm files were moved
print(f"✅ Files moved to Risk Levels:\n- Safe: {len(safe_files)}\n- Medium: {len(medium_files)}\n- High: {len(high_files)}")
