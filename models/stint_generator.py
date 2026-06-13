class StintGenerator:
    def generate(self, current_lap, total_laps):
        """
        Generates sensible 1-stop and 2-stop combinations based on remaining laps.
        In a real scenario, this would use constraint solvers, but we generate the F1 core paths.
        """
        remaining = total_laps - current_lap
        if remaining <= 0:
            return []

        strategies = []
        
        # Scenario 1: Push Stint (Soft -> End) if less than 20 laps
        if remaining < 20:
            strategies.append({
                "name": "PUSH_STINT",
                "stints": [{"compound": "SOFT", "laps": remaining, "push_level": 0.9}]
            })
            
        # Scenario 2: 1-Stop Undercut
        stint1_laps = int(remaining * 0.4)
        stint2_laps = remaining - stint1_laps
        strategies.append({
            "name": "UNDERCUT_1_STOP",
            "stints": [
                {"compound": "MEDIUM", "laps": stint1_laps, "push_level": 0.8},
                {"compound": "HARD", "laps": stint2_laps, "push_level": 0.7}
            ]
        })
        
        # Scenario 3: 1-Stop Overcut
        stint1_laps = int(remaining * 0.6)
        stint2_laps = remaining - stint1_laps
        strategies.append({
            "name": "OVERCUT_1_STOP",
            "stints": [
                {"compound": "HARD", "laps": stint1_laps, "push_level": 0.7},
                {"compound": "MEDIUM", "laps": stint2_laps, "push_level": 0.8}
            ]
        })

        return strategies
