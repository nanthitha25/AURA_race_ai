import pandas as pd
import numpy as np
import os

def braking_aggression(data):
    # Avoid division by zero by replacing 0 speed with a small number
    safe_speed = data["Speed"].replace(0, 1)
    # The prompt formula: Brake Pressure / Speed Before Brake
    # Assuming 'Brake' is boolean or 0-100, we'll treat it as float
    score = (data["Brake"].astype(float) / safe_speed)
    # Scale it up slightly for readability
    return score.mean() * 100

def throttle_commitment(data):
    return data["Throttle"].mean() / 100.0  # normalize 0-1

def speed_consistency(data):
    variation = data["Speed"].std()
    if pd.isna(variation):
        variation = 0
    score = 1 / (1 + variation)
    return score

def corner_risk(data):
    # The prompt formula: (Brake.mean() + Throttle.mean()) / 2
    risk = (data["Brake"].astype(float).mean() + data["Throttle"].astype(float).mean())
    return risk / 2.0 / 100.0 # normalize 0-1 assuming 0-100 scale

def main():
    print("Starting Feature Engineering...")
    # Construct path to the data file
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "verstappen_telemetry.csv")
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    # Load telemetry
    data = pd.read_csv(data_path)
    
    # Calculate features for VER
    ver_brake_aggression = braking_aggression(data)
    ver_throttle = throttle_commitment(data)
    ver_consistency = speed_consistency(data)
    ver_risk = corner_risk(data)

    print(f"VER Features calculated:")
    print(f"Brake Aggression: {ver_brake_aggression:.2f}")
    print(f"Throttle Commitment: {ver_throttle:.2f}")
    print(f"Consistency: {ver_consistency:.2f}")

    # Build dataset including dummy data for NOR and HAM as per prompt example
    # so we have enough data to train the model
    profiles = [
        {"Driver": "VER", "Brake Aggression": round(ver_brake_aggression, 2), "Throttle": round(ver_throttle, 2), "Consistency": round(ver_consistency, 2), "Risk Index": round(ver_risk, 2)},
        {"Driver": "NOR", "Brake Aggression": 0.70, "Throttle": 0.88, "Consistency": 0.95, "Risk Index": 0.75},
        {"Driver": "HAM", "Brake Aggression": 0.75, "Throttle": 0.86, "Consistency": 0.90, "Risk Index": 0.72},
        # Adding a few more to help ML
        {"Driver": "LEC", "Brake Aggression": 0.80, "Throttle": 0.90, "Consistency": 0.88, "Risk Index": 0.80},
        {"Driver": "RUS", "Brake Aggression": 0.78, "Throttle": 0.85, "Consistency": 0.85, "Risk Index": 0.75},
        {"Driver": "SAI", "Brake Aggression": 0.72, "Throttle": 0.84, "Consistency": 0.92, "Risk Index": 0.70},
    ]

    df_profiles = pd.DataFrame(profiles)
    print("\nDriver DNA Dataset:")
    print(df_profiles)

    # Save to data directory
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "driver_profile.csv")
    df_profiles.to_csv(output_path, index=False)
    print(f"\nSaved driver profiles to {output_path}")

if __name__ == "__main__":
    main()
