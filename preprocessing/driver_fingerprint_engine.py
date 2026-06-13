import pandas as pd
import numpy as np
import os

def generate_driver_fingerprints():
    print("Generating Real Driver Fingerprints...")
    
    # Check if the dataset exists (since the orchestrator might still be running)
    data_path = "data/processed/aura_raw_race_dataset.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please wait for the dataset builder to finish.")
        return

    data = pd.read_csv(data_path)

    def calculate_driver_features(driver_data):
        features = {}
        
        # Brake aggression
        if "Brake" in driver_data.columns and not driver_data["Brake"].empty:
            features["brake_aggression"] = driver_data["Brake"].mean() / 100.0
        else:
            features["brake_aggression"] = 0.5
            
        # Throttle commitment
        if "Throttle" in driver_data.columns and not driver_data["Throttle"].empty:
            features["throttle_commitment"] = driver_data["Throttle"].mean() / 100.0
        else:
            features["throttle_commitment"] = 0.5
            
        # Speed profile & Risk
        if "Speed" in driver_data.columns and not driver_data["Speed"].empty:
            mean_speed = driver_data["Speed"].mean()
            std_speed = driver_data["Speed"].std()
            
            features["average_speed"] = mean_speed
            
            if mean_speed > 0:
                features["corner_risk"] = std_speed / mean_speed
                features["consistency"] = 1 - (std_speed / mean_speed)
            else:
                features["corner_risk"] = 0.5
                features["consistency"] = 0.5
        else:
            features["average_speed"] = 0
            features["corner_risk"] = 0.5
            features["consistency"] = 0.5

        return features

    driver_profiles = []
    
    for driver in data["Driver"].unique():
        driver_data = data[data["Driver"] == driver]
        profile = calculate_driver_features(driver_data)
        profile["Driver"] = driver
        driver_profiles.append(profile)

    fingerprint = pd.DataFrame(driver_profiles)
    
    # Save output
    os.makedirs("data/processed", exist_ok=True)
    out_file = "data/processed/driver_fingerprint.csv"
    fingerprint.to_csv(out_file, index=False)
    
    print(f"Driver fingerprint generated and saved to {out_file}")
    print(fingerprint.head())

if __name__ == "__main__":
    generate_driver_fingerprints()
