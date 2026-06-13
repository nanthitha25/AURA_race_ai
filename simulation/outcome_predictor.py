from simulation.scenario_generator import generate_scenarios
from simulation.race_simulator import RaceSimulator

class OutcomePredictor:
    def __init__(self, overtake_ai, mistake_prob, overtake_prob):
        self.simulator = RaceSimulator(overtake_ai, mistake_prob, overtake_prob)
        self.scenarios = generate_scenarios()

    def evaluate_strategies(self, current_state):
        results = []
        
        for action in self.scenarios:
            outcome = self.simulator.simulate(current_state, action)
            
            # Custom Reward Function
            score = (
                (outcome["position_gain"] * 50) + 
                (outcome["confidence"] * 30) - 
                (outcome["risk"] * 20)
            )
            
            outcome["score"] = float(score)
            results.append(outcome)
            
        # Sort by best score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
