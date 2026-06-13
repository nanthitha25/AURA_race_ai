import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.psychological_memory import PsychologicalMemory
from models.knowledge_graph import OpponentKnowledgeGraph
from models.overtake_predictor import OvertakePredictor
from simulation.outcome_predictor import OutcomePredictor
from simulation.race_state import get_mock_race_state
from simulation.multi_stint_simulator import MultiStintSimulator

class AuraDecisionEngine:
    def __init__(self):
        self.memory = PsychologicalMemory()
        self.knowledge = OpponentKnowledgeGraph()
        self.overtake_ai = OvertakePredictor()

    def decide(self, driver, opponent, gap, speed_delta, mistake_probability, tyre_advantage, drs_available, corner_factor):
        
        # 1. Psychological Memory Adjustment
        pressure_factor = self.memory.pressure_factor(opponent)
        adjusted_mistake_prob = min(1.0, mistake_probability * (1 + pressure_factor))
        
        # 2. Knowledge Graph Weakness
        weakness_area = self.knowledge.best_attack_area(opponent)
        weakness_severity = self.knowledge.weakness_severity(opponent)
        
        # 3. Overtake Predictor ML
        overtake_probability = self.overtake_ai.predict(
            gap=gap,
            speed_delta=speed_delta,
            tyre_delta=tyre_advantage,
            drs=int(drs_available),
            opponent_weakness=weakness_severity,
            pressure_level=adjusted_mistake_prob,
            corner_factor=corner_factor
        )
        
        # 4. Counterfactual Simulation
        current_state = get_mock_race_state()
        current_state["gap_ahead"] = gap
        current_state["opponent"] = opponent
        
        predictor = OutcomePredictor(self.overtake_ai, adjusted_mistake_prob, overtake_probability)
        evaluated_futures = predictor.evaluate_strategies(current_state)
        
        # 5. Multi-Stint Optimization (Phase 10.5)
        # Using mock lap 52/78 for Monaco
        stint_sim = MultiStintSimulator()
        multi_stint_plans = stint_sim.simulate(current_lap=52, total_laps=78, track="Monaco", current_position=4)
        
        # The best future is the first in the sorted list
        best_strategy = evaluated_futures[0]
        
        return {
            "action": best_strategy["action"],
            "confidence": float(round(best_strategy["confidence"] * 100, 1)),
            "expected_position": best_strategy["expected_position"],
            "overtake_probability": float(round(overtake_probability * 100, 1)),
            "mistake_probability": float(round(adjusted_mistake_prob * 100, 1)),
            "weakness_detected": weakness_area,
            "risk": best_strategy.get("risk", 0.5),
            "evaluated_futures": evaluated_futures,
            "multi_stint_plans": multi_stint_plans
        }
