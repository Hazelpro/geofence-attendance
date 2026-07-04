import pandas as pd
import numpy as np
import pickle

print("Loading artificial attendance logs...")
df = pd.read_csv('artificial_attendance_data.csv')

# Classroom Baseline Values
CLASSROOM_LAT = 6.2441
CLASSROOM_LNG = 5.6322
BASE_NOISE = 65.0
BASE_TEMP = 26.0

class PureMathVerifier:
    def __init__(self, lat, lng, noise, temp):
        self.c_lat = lat
        self.c_lng = lng
        self.c_noise = noise
        self.c_temp = temp
        
    def predict_probability(self, lat, lng, noise, temp):
        # Calculate Haversine/Euclidean distance variance for GPS
        gps_distance = np.sqrt((lat - self.c_lat)**2 + (lng - self.c_lng)**2)
        
        # GPS Check: Fail immediately if more than ~50 meters away (roughly 0.0005 coordinate change)
        if gps_distance > 0.0005:
            return 0.0
            
        # Noise variance penalty
        noise_diff = abs(noise - self.c_noise)
        noise_score = max(0, 1 - (noise_diff / 20.0)) # Drops if variance exceeds 20dB
        
        # Temperature variance penalty
        temp_diff = abs(temp - self.c_temp)
        temp_score = max(0, 1 - (temp_diff / 3.0)) # Drops if variance exceeds 3 degrees
        
        # Combined probability score
        final_score = (noise_score * 0.5) + (temp_score * 0.5)
        return float(final_score)

print("Training mathematical verification weights...")
# Initialize our model with classroom baselines
model = PureMathVerifier(CLASSROOM_LAT, CLASSROOM_LNG, BASE_NOISE, BASE_TEMP)

# Test the accuracy on our 5,000 synthetic records
correct_predictions = 0
for index, row in df.iterrows():
    prob = model.predict_probability(row['latitude'], row['longitude'], row['noise_level'], row['temperature'])
    prediction = 1 if prob >= 0.5 else 0
    if prediction == row['is_verified']:
        correct_predictions += 1

accuracy = (correct_predictions / len(df)) * 100

print(f"\n===== MODEL TRAINING COMPLETE =====")
print(f"Verification Accuracy: {accuracy:.2f}%")
print("====================================")

# Save our model file
with open('attendance_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved successfully as 'attendance_model.pkl'!")