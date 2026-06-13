import pandas as pd
import os
import numpy as np

def detect_battles(laps_df):
    """
    Detects when drivers are battling under pressure.
    Input: laps DataFrame (from data/raw/laps)
    """
    print("Detecting Battle & Pressure Events...")
    events = []
    
    # Needs Track and Year from filename context, but we can assume they are passed or infer
    # Group by LapNumber
    for lap_num, lap_group in laps_df.groupby('LapNumber'):
        if 'LapStartTime_s' not in lap_group.columns:
            continue
            
        lap_group = lap_group.sort_values(by='LapStartTime_s', na_position='last')
        
        previous_time = None
        previous_driver = None
        
        for idx, row in lap_group.iterrows():
            driver = row.get('Driver', row.get('DriverNumber'))
            current_time = row['LapStartTime_s']
            
            if pd.notna(previous_time) and pd.notna(current_time):
                gap = current_time - previous_time
                if 0 < gap <= 1.0:
                    events.append({
                        "Driver": previous_driver,
                        "Opponent": driver,
                        "Lap": lap_num,
                        "Gap": round(gap, 3),
                        "Pressure": "HIGH"
                    })
            
            previous_time = current_time
            previous_driver = driver

    events_df = pd.DataFrame(events)
    if not events_df.empty:
        out_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "pressure_events.csv")
        events_df.to_csv(out_path, index=False)
        print(f"Detected {len(events_df)} pressure events! Saved to {out_path}")
    else:
        print("No pressure events detected.")
    
    return events_df
