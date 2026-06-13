class OpportunityMapper:
    def map_weakness(self, weakness_profile, lap):
        """
        Maps a static driver weakness to a dynamic severity multiplier
        based on the current lap context.
        """
        # Base severity from Knowledge Graph
        base_severity = weakness_profile.get("severity", 0.5)
        corner = weakness_profile.get("corner", "T10")
        
        # Determine multiplier based on tyre phase
        if 43 <= lap <= 47:
            multiplier = 0.95 # Peak tyre degradation
        elif 48 <= lap <= 52:
            multiplier = 0.70
        else:
            multiplier = 0.40 # Stable
            
        return {
            "corner": corner,
            "severity": min(1.0, base_severity * multiplier)
        }
