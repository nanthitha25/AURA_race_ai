import pandas as pd
import os

def detect_pressure_events():
    """
    Simulates scanning historical lap telemetry for "Pressure Events" (gap < 1.0s for > 2 laps).
    """
    print("Scanning gap history for pressure events...")
    
    # Simulate detected events
    events = [
        {"gap": 0.35, "lap_pressure": 5, "brake_variation": 18, "steering_error": 12, "tire_age": 25, "mistake": 1},
        {"gap": 0.80, "lap_pressure": 2, "brake_variation": 5, "steering_error": 4, "tire_age": 10, "mistake": 0},
        {"gap": 0.40, "lap_pressure": 4, "brake_variation": 15, "steering_error": 10, "tire_age": 20, "mistake": 1},
        {"gap": 0.95, "lap_pressure": 1, "brake_variation": 2, "steering_error": 2, "tire_age": 5, "mistake": 0},
        {"gap": 0.20, "lap_pressure": 6, "brake_variation": 25, "steering_error": 15, "tire_age": 30, "mistake": 1},
    ]
    
    df = pd.DataFrame(events)
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "pressure_events.csv")
    df.to_csv(data_path, index=False)
    print(f"Detected {len(df)} pressure events. Saved to {data_path}")

if __name__ == "__main__":
    detect_pressure_events()
