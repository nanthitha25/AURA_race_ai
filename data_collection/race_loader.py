import os
import fastf1
import pandas as pd

# Ensure FastF1 uses the cache
cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'f1_cache')
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

def fetch_race_session(year, track):
    """
    Fetches the race session for a specific year and track.
    Saves lap data and results to data/raw/
    Returns the session object for telemetry extraction.
    """
    print(f"Loading session data for {year} {track}...")
    try:
        session = fastf1.get_session(year, track, 'R')
        session.load()
        
        laps = session.laps.copy()
        laps['LapStartTime_s'] = laps['LapStartTime'].dt.total_seconds()
        laps_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "laps", f"{year}_{track.lower()}.csv")
        # Keep numeric/string columns that can be saved easily
        saveable_laps = laps.drop(columns=['Time', 'LapTime', 'PitOutTime', 'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'Sector1SessionTime', 'Sector2SessionTime', 'Sector3SessionTime', 'LapStartTime'], errors='ignore')
        saveable_laps.to_csv(laps_path, index=False)
        
        # Save Results
        results = session.results
        results_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "results", f"{year}_{track.lower()}_results.csv")
        saveable_results = results.drop(columns=['Time', 'Q1', 'Q2', 'Q3'], errors='ignore')
        saveable_results.to_csv(results_path, index=False)
        
        print(f"Saved Laps to {laps_path} and Results to {results_path}")
        return session
    except Exception as e:
        print(f"Failed to fetch session {year} {track}: {e}")
        return None

if __name__ == "__main__":
    # Test loading
    fetch_race_session(2024, "Monaco")
