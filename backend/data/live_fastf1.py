import fastf1
import pandas as pd
import os

class FastF1Collector:
    def __init__(self, year, gp):
        self.year = year
        self.gp = gp
        fastf1.Cache.enable_cache(os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache"))

    def load_session(self):
        session = fastf1.get_session(self.year, self.gp, "R")
        session.load()
        return session

    def get_driver_telemetry(self, driver):
        session = self.load_session()
        laps = session.laps
        driver_laps = laps[laps.Driver == driver]
        
        if driver_laps.empty:
            print(f"No laps found for {driver}")
            return None
            
        fastest_lap = driver_laps.pick_fastest()
        telemetry = fastest_lap.get_telemetry()
        
        return telemetry
