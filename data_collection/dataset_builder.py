import pandas as pd
import os
import numpy as np

def build_driver_fingerprints(telemetry_df):
    """
    Analyzes raw telemetry and extracts Driver DNA (Aggression, Consistency, Risk).
    """
    print("Building Driver Fingerprints from raw telemetry...")
    
    drivers = telemetry_df['Driver'].unique()
    fingerprints = []
    
    for driver in drivers:
        df_d = telemetry_df[telemetry_df['Driver'] == driver]
        
        # Calculate DNA Metrics
        avg_brake = df_d['Brake'].mean()
        max_brake = df_d['Brake'].max()
        throttle_commitment = (df_d['Throttle'] == 100).mean() * 100
        speed_var = df_d['Speed'].std()
        
        # Normalization logic
        aggression = min(0.99, (max_brake / 100.0) * 0.5 + (throttle_commitment / 100.0) * 0.5)
        consistency = max(0.5, 1.0 - (speed_var / 300.0))
        risk = "High" if aggression > 0.85 else "Medium" if aggression > 0.75 else "Low"
        
        fingerprints.append({
            "Driver": driver,
            "Late_braking": round(aggression * 95, 1),
            "Throttle_commitment": round(throttle_commitment, 1),
            "Aggression": round(aggression, 2),
            "Consistency": round(consistency, 2),
            "Risk": risk
        })
        
    fingerprint_df = pd.DataFrame(fingerprints)
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "driver_fingerprint_real.csv")
    fingerprint_df.to_csv(out_path, index=False)
    print(f"Generated fingerprints for {len(drivers)} drivers. Saved to {out_path}")
    return fingerprint_df
