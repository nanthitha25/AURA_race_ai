import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.overtake_opportunity_score import OvertakeOpportunityScore
from features.lap_window_engine import LapWindowEngine
from features.opportunity_mapper import OpportunityMapper

class OpportunityEngine:
    def __init__(self):
        self.scorer = OvertakeOpportunityScore()
        self.window_engine = LapWindowEngine()
        self.mapper = OpportunityMapper()

    def evaluate(self, current_state, base_weakness_profile):
        """
        Simulates the next N laps to find the best OOS (Overtake Opportunity Score).
        """
        opportunities = []
        
        for lap_ahead in range(1, 6): # Look ahead 5 laps
            future_state = current_state.copy()
            future_state["lap"] += lap_ahead
            
            # Predict tyre delta decreasing slightly over time
            future_state["tyre_age_advantage"] = max(0, future_state.get("tyre_age_advantage", 2) - (lap_ahead * 0.1))
            
            # Predict DRS remaining same
            future_state["drs"] = future_state.get("drs", True)
            
            # Predict Gap (mock physics for simulation, assumes gap closes)
            future_state["gap"] = max(0.1, future_state.get("gap", 0.5) - (lap_ahead * 0.05))
            
            # Calculate Lap Window Factor
            future_state["lap_window_factor"] = self.window_engine.compute(future_state["lap"])
            
            # Calculate Dynamic Weakness
            dynamic_weakness = self.mapper.map_weakness(base_weakness_profile, future_state["lap"])
            
            # Calculate Final OOS
            score = self.scorer.calculate(future_state, dynamic_weakness)
            
            opportunities.append({
                "lap": future_state["lap"],
                "score": score,
                "corner": dynamic_weakness["corner"],
                "drs_available": future_state["drs"],
                "gap_predicted": round(future_state["gap"], 2)
            })

        best_opportunity = max(opportunities, key=lambda x: x["score"])
        return best_opportunity, opportunities
