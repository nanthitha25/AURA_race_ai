import json
import os

class DigitalDriver:
    def __init__(self, driver):
        self.driver = driver
        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "database", "digital_driver_twins.json")
        with open(db_path, "r") as f:
            data = json.load(f)
            self.profile = data.get(driver, {})

    def predict_reaction(self, situation):
        pressure = situation.get("pressure", "LOW")
        corner = situation.get("corner", "General")
        
        # Pull defensive style
        defense = self.profile.get("defense_style", {}).get("preferred", "normal_line")
        
        if pressure == "HIGH":
            # Very deterministic logic based on Twin DB
            if defense == "inside_line":
                return {
                    "predicted_action": "inside_defense",
                    "confidence": 0.78,
                    "counter_strategy": "outside_attack"
                }
            elif defense == "late_braking":
                return {
                    "predicted_action": "aggressive_defense",
                    "confidence": 0.85,
                    "counter_strategy": "switchback"
                }

        return {
            "predicted_action": "normal",
            "confidence": 0.60,
            "counter_strategy": "standard_overtake"
        }
