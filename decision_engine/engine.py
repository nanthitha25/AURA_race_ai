from decision_engine.strategy_rules import evaluate_strategy
from decision_engine.confidence import calculate_confidence

class DecisionEngine:
    def __init__(self, mistake_probability, gap, tire_advantage, driver_style, drs=True):
        self.mistake_probability = mistake_probability
        self.gap = gap
        self.tire_advantage = tire_advantage
        self.driver_style = driver_style
        self.drs = drs

    def generate_strategy(self):
        data = {
            "gap": self.gap,
            "mistake_probability": self.mistake_probability,
            "tire_advantage": self.tire_advantage,
            "drs": self.drs,
            "tire_temperature": 90 # Hardcoded for now
        }
        
        action, reason = evaluate_strategy(data)
        confidence = calculate_confidence(self.mistake_probability, self.gap, self.driver_style)
        
        return {
            "action": action,
            "reason": reason,
            "confidence": confidence
        }
