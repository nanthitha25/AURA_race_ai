import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.stint_generator import StintGenerator
from models.tyre_degradation_model import TyreDegradationModel
from models.pit_strategy_optimizer import PitStrategyOptimizer

class MultiStintSimulator:
    def __init__(self):
        self.generator = StintGenerator()
        self.tyre_model = TyreDegradationModel()
        self.pit_model = PitStrategyOptimizer()

    def simulate(self, current_lap, total_laps, track="Monaco", base_lap_time=75.0, current_position=4):
        """
        Evaluates all multi-stint strategies and returns the lowest total race time.
        """
        strategies = self.generator.generate(current_lap, total_laps)
        evaluated = []

        for strategy in strategies:
            total_race_time = 0
            stops = len(strategy["stints"]) - 1
            
            for i, stint in enumerate(strategy["stints"]):
                # 1. Base time
                stint_time = base_lap_time * stint["laps"]
                
                # 2. Tyre degradation loss
                deg_time = self.tyre_model.calculate_time_loss(stint["compound"], stint["laps"], stint["push_level"])
                stint_time += deg_time
                
                total_race_time += stint_time
                
            # 3. Pit stop cost
            pit_loss = self.pit_model.calculate_pit_cost(track) * stops
            total_race_time += pit_loss
            
            # 4. Traffic Penalty (simulated heuristic)
            traffic_risk = self.pit_model.calculate_traffic_risk(current_position + (stops * 2))
            traffic_penalty = traffic_risk * 10.0 # lose 10s if stuck in traffic
            total_race_time += traffic_penalty
            
            # Convert time into a relative "score" (lower time = higher score)
            # Baseline is roughly remaining_laps * base_lap_time
            expected_time = (total_laps - current_lap) * base_lap_time
            delta = expected_time - total_race_time
            confidence = min(100.0, max(0.0, 50 + (delta * 2)))

            # Estimate Finish Position
            if delta > 10:
                expected_finish = max(1, current_position - 2)
            elif delta > 0:
                expected_finish = max(1, current_position - 1)
            else:
                expected_finish = current_position
            
            evaluated.append({
                "name": strategy["name"],
                "stints": strategy["stints"],
                "total_time": round(total_race_time, 2),
                "confidence": round(confidence, 1),
                "expected_finish": expected_finish,
                "traffic_risk": traffic_risk
            })

        # Return sorted by highest confidence
        if not evaluated:
            return None
            
        evaluated.sort(key=lambda x: x["confidence"], reverse=True)
        return evaluated
