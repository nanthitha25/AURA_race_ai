import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from decision_engine.aura_decision_engine import AuraDecisionEngine
from decision_engine.radio_generator import generate_radio_message
from models.digital_twin.digital_driver import DigitalDriver
from models.race_outcome_predictor import RaceOutcomePredictor

class MasterRaceAgent:
    def __init__(self, mistake_ai):
        self.mistake_ai = mistake_ai # XGBoost model passed from fastAPI
        self.decision_engine = AuraDecisionEngine()
        self.outcome_predictor = RaceOutcomePredictor()

    def process(self, telemetry, features):
        
        # 1. Base ML Inference
        mistake_probability = self.mistake_ai.predict_mistake(features)
        
        driver = telemetry.get("driver", "VER")
        opponent = telemetry.get("opponent", "NOR")
        
        # 2. Strategy Engine (Psychology + Knowledge + Overtake + Counterfactual)
        strategy_decision = self.decision_engine.decide(
            driver=driver,
            opponent=opponent,
            gap=features["gap"],
            speed_delta=8, # Mock speed delta
            mistake_probability=mistake_probability,
            tyre_advantage=2, # Mock tyre delta
            drs_available=bool(telemetry.get("drs", 0)),
            corner_factor=0.78
        )
        
        # 3. Digital Driver Twin
        pressure_level = "HIGH" if mistake_probability > 0.4 else "LOW"
        twin = DigitalDriver(opponent)
        opponent_reaction = twin.predict_reaction({"pressure": pressure_level, "corner": "General"})
        
        # 4. Race Outcome Forecast
        race_forecast = self.outcome_predictor.predict(
            lap=telemetry.get("lap", 52),
            position=telemetry.get("position", 4),
            gap_ahead=features["gap"],
            gap_behind=1.5,
            tyre_age=15,
            pace_delta=-0.4,
            pit_stops=1,
            weather=0
        )
        
        # Top predicted position
        best_finish = list(race_forecast.keys())[0]
        finish_probability = round(race_forecast[best_finish] * 100, 1)
        
        # 5. Radio Recommendation
        radio = generate_radio_message(strategy_decision)
        
        # 6. Holistic Output
        return {
            "driver": driver,
            "opponent": opponent,
            "speed": telemetry.get("speed"),
            "throttle": telemetry.get("throttle"),
            "brake": telemetry.get("brake"),
            "gap": features.get("gap", 0.38),
            "gear": telemetry.get("gear", 8),
            "rpm": telemetry.get("rpm", 11500),
            "drs": bool(telemetry.get("drs", 0)),
            "mistake_probability": float(round(mistake_probability * 100, 2)),
            "decision": strategy_decision,
            "twin_prediction": opponent_reaction,
            "race_forecast": {
                "predicted_position": best_finish,
                "probability": finish_probability
            },
            "agents": {
                "strategy": {"action": strategy_decision["action"], "confidence": strategy_decision["confidence"]},
                "psychology": {"status": "Vulnerable" if mistake_probability > 0.3 else "Stable", "confidence": float(round(mistake_probability * 100, 2))},
                "overtake": {"action": "Attack T10", "confidence": 88.4},
                "risk": {"status": "Approved" if strategy_decision["risk"] < 0.5 else "Rejected", "confidence": float(round(100 - (strategy_decision["risk"]*100), 1))}
            },
            "radio": radio,
            "timestamp": telemetry.get("time")
        }
