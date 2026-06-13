import random

class RaceSimulator:
    def __init__(self, overtake_ai, mistake_prob, overtake_prob):
        # We inject the current AI predictions into the simulator
        self.mistake_prob = mistake_prob
        self.overtake_prob = overtake_prob

    def simulate(self, state, action):
        
        # Attack Simulation
        if action == "ATTACK":
            # Success is heavily tied to the true Overtake Probability
            success = self.overtake_prob + random.uniform(-0.1, 0.1)
            position_gain = 1 if success > 0.65 else 0
            risk = 0.20 if position_gain == 1 else 0.40 # Higher risk if attack fails
            confidence = success

        # Pressure Simulation
        elif action == "PRESSURE":
            success = self.mistake_prob + random.uniform(-0.1, 0.1)
            position_gain = 1 if success > 0.85 else 0
            risk = 0.05
            confidence = success
            
        # Pit Stop Simulation
        elif action == "PIT":
            # Pitting guarantees losing positions short term, gaining long term.
            # We mock a short-term loss for now.
            position_gain = -2 
            risk = 0.01
            confidence = 0.95
            
        # Defend Simulation
        elif action == "DEFEND":
            position_gain = 0
            risk = 0.10
            confidence = 0.80
            
        # Save Tyres Simulation
        elif action == "SAVE":
            position_gain = 0
            risk = 0.02
            confidence = 0.90
            
        else:
            position_gain = 0
            risk = 0.0
            confidence = 0.0

        return {
            "action": action,
            "expected_position": int(max(1, state["position"] - position_gain)), # Lower position number is better
            "position_gain": int(position_gain),
            "confidence": float(min(1.0, max(0.0, confidence))),
            "risk": float(risk)
        }
