import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_collection.race_loader import fetch_race_session
from data_collection.telemetry_extractor import extract_driver_telemetry, get_drivers
from data_collection.battle_detector import detect_battles
from data_collection.dataset_builder import build_driver_fingerprints

def build_dataset(years, races):
    """
    Master pipeline to collect multiple years, races, and all drivers.
    """
    print(f"Starting Real Dataset Build: Years={years}, Races={races}")
    
    all_telemetry = []
    
    for year in years:
        for track in races:
            session = fetch_race_session(year, track)
            if not session:
                continue
                
            drivers = get_drivers(session)
            print(f"Grid found: {drivers}")
            
            for driver in drivers:
                tel_df = extract_driver_telemetry(session, driver, year, track)
                if tel_df is not None:
                    all_telemetry.append(tel_df)
                    
            # Detect battles from the saved laps file
            laps_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "laps", f"{year}_{track.lower()}.csv")
            if os.path.exists(laps_path):
                laps_df = pd.read_csv(laps_path)
                detect_battles(laps_df)
                    
    if all_telemetry:
        final_df = pd.concat(all_telemetry, ignore_index=True)
        final_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "aura_raw_race_dataset.csv")
        final_df.to_csv(final_path, index=False)
        print(f"Saved massive telemetry dataset to {final_path} with {len(final_df)} rows.")
        
        # Build Fingerprints
        build_driver_fingerprints(final_df)
    else:
        print("Dataset build failed: No data extracted.")

if __name__ == "__main__":
    # Test run on a tiny subset to verify it works without hours of downloading
    test_years = [2024]
    test_races = ["Monaco"]
    
    build_dataset(years=test_years, races=test_races)
