import os
import pandas as pd

def get_drivers(session):
    """Returns a list of all driver abbreviations from the session."""
    drivers = []
    for driver_num in session.drivers:
        info = session.get_driver(driver_num)
        drivers.append(info["Abbreviation"])
    return drivers

def extract_driver_telemetry(session, driver, year, track):
    """
    Extracts high-resolution telemetry for a specific driver from a loaded session.
    Saves the telemetry to data/raw/telemetry/
    """
    print(f"  -> Extracting telemetry for {driver} at {year} {track}...")
    
    try:
        driver_laps = session.laps.pick_driver(driver)
        all_telemetry = []
        for lap_num in driver_laps['LapNumber'].dropna().unique():
            try:
                lap = driver_laps[driver_laps['LapNumber'] == lap_num].iloc[0]
                telemetry = lap.get_telemetry()
                
                filtered = telemetry[['Speed', 'Throttle', 'Brake', 'RPM', 'nGear', 'DRS', 'Distance', 'Time']].copy()
                filtered['Driver'] = driver
                filtered['Lap'] = lap_num
                filtered['Year'] = year
                filtered['Track'] = track
                filtered['Time_s'] = filtered['Time'].dt.total_seconds()
                filtered = filtered.drop(columns=['Time'])
                
                all_telemetry.append(filtered)
            except Exception as e:
                pass
                
        if all_telemetry:
            combined_telemetry = pd.concat(all_telemetry, ignore_index=True)
            out_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "telemetry", f"{driver}_{track.lower()}_{year}.csv")
            combined_telemetry.to_csv(out_path, index=False)
            return combined_telemetry
        return None
    except Exception as e:
        print(f"Failed to extract telemetry for {driver}: {e}")
        return None
