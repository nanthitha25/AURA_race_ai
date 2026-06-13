class PitStrategyOptimizer:
    def calculate_pit_cost(self, track="Monaco"):
        """
        Returns the flat time penalty of doing a pit stop.
        """
        if track == "Monaco":
            return 26.0
        elif track == "Silverstone":
            return 28.5
        else:
            return 25.0

    def calculate_traffic_risk(self, estimated_rejoin_position):
        """
        Models the probability of rejoining the track into dirty air/traffic.
        """
        if estimated_rejoin_position > 8:
            return 0.7  # High risk of traffic
        if estimated_rejoin_position > 4:
            return 0.4
        return 0.1  # Rejoining in clean air
