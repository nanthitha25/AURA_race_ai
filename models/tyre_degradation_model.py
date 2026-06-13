class TyreDegradationModel:
    def calculate_time_loss(self, compound, laps, push_level):
        """
        Calculates the accumulated time lost (in seconds) over the entire stint due to tyre degradation.
        """
        # Base degradation rate per lap
        if compound == "SOFT":
            base_deg = 0.08
        elif compound == "MEDIUM":
            base_deg = 0.05
        else: # HARD
            base_deg = 0.03
            
        # Higher push level = exponentially worse degradation
        push_penalty = push_level ** 1.5
        
        deg_per_lap = base_deg * push_penalty
        
        # Total time loss is the integral of degradation over the laps
        total_time_lost = (deg_per_lap * (laps ** 2)) / 2
        return total_time_lost
