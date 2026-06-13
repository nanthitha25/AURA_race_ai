class OvertakeOpportunityScore:
    def calculate(self, state, weakness_profile):
        """
        Calculates the Overtake Opportunity Score (OOS).
        Max score ~ 100.
        """
        gap_score = max(0, (1.0 - state.get("gap", 1.0))) * 30
        tyre_score = max(0, state.get("tyre_age_advantage", 0)) * 2
        drs_score = 15 if state.get("drs") else 0
        
        # Weakness specific to corner
        corner_score = weakness_profile.get("severity", 0.5) * 25
        
        pressure_score = state.get("opponent_pressure", 0.0) * 20
        
        lap_window_score = state.get("lap_window_factor", 0.5) * 10

        oos = (
            gap_score +
            tyre_score +
            drs_score +
            corner_score +
            pressure_score +
            lap_window_score
        )
        return min(100.0, oos)
