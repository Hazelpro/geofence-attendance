import pandas as pd
import numpy as np

# Target: 5,000 artificial records
n_samples = 5000

# Fixed Reference Classroom Core Coordinates
CLASSROOM_LAT = 6.2441
CLASSROOM_LNG = 5.6322
CLASSROOM_BASE_NOISE = 65.0  # Decibel baseline during a crowded lecture
CLASSROOM_BASE_TEMP = 26.0   # Target room temperature (Celsius)

data = []

for _ in range(n_samples):
    # 50% chance the student is actually in class, 50% chance they are spoofing
    is_present = np.random.choice([1, 0])
    
    if is_present == 1:
        # Authentic check-in: Right inside the room, noise and temp match perfectly
        lat = CLASSROOM_LAT + np.random.normal(0, 0.0001)
        lng = CLASSROOM_LNG + np.random.normal(0, 0.0001)
        noise = CLASSROOM_BASE_NOISE + np.random.normal(0, 4.0)
        temp = CLASSROOM_BASE_TEMP + np.random.normal(0, 0.5)
    else:
        # Fraudulent check-in attempt variations
        spoof_type = np.random.choice(['wrong_gps', 'wrong_noise', 'wrong_both'])
        
        if spoof_type == 'wrong_gps':
            # Remote location, but matched noise (maybe using a recording tool)
            lat = CLASSROOM_LAT + np.random.uniform(0.01, 0.05)
            lng = CLASSROOM_LNG + np.random.uniform(0.01, 0.05)
            noise = CLASSROOM_BASE_NOISE + np.random.normal(0, 2.0)
            temp = CLASSROOM_BASE_TEMP + np.random.normal(0, 0.5)
        elif spoof_type == 'wrong_noise':
            # Right location (spoofed GPS app), but sitting in a dead quiet room at home
            lat = CLASSROOM_LAT + np.random.normal(0, 0.0001)
            lng = CLASSROOM_LNG + np.random.normal(0, 0.0001) # Added missing longitude line here
            noise = 32.0 + np.random.normal(0, 3.0) 
            temp = CLASSROOM_BASE_TEMP + np.random.normal(0, 0.5)
        else:
            # Entirely wrong parameters (trying to check in from a distance normally)
            lat = CLASSROOM_LAT + np.random.uniform(0.01, 0.05)
            lng = CLASSROOM_LNG + np.random.uniform(0.01, 0.05) # Added missing longitude line here too
            noise = 35.0 + np.random.normal(0, 4.0)
            temp = 31.0 + np.random.normal(0, 1.5)

    data.append([lat, lng, noise, temp, is_present])

# Package and build the dataset
df = pd.DataFrame(data, columns=['latitude', 'longitude', 'noise_level', 'temperature', 'is_verified'])
df.to_csv('artificial_attendance_data.csv', index=False)
print("Artificial database file successfully populated with 5,000 entries!")