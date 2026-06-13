import json
import os

class PsychologicalMemory:
    def __init__(self):
        memory_path = os.path.join(os.path.dirname(__file__), "..", "database", "driver_memory.json")
        with open(memory_path, 'r') as file:
            self.memory = json.load(file)

    def get_driver_profile(self, driver):
        if driver in self.memory:
            return self.memory[driver]
        return None

    def pressure_factor(self, driver):
        profile = self.get_driver_profile(driver)
        if profile is None:
            return 0.5  # Neutral factor for unknown drivers

        # Calculate historical mistake rate under pressure
        mistake_rate = profile["mistakes"] / max(1, profile["pressure_events"])
        return mistake_rate
