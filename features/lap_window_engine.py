class LapWindowEngine:
    def compute(self, lap):
        """
        Returns a multiplier for attack windows based on lap phases.
        E.g. Lap 40-50 represents a prime tire degradation cliff phase.
        """
        if 40 <= lap <= 50:
            return 1.0  # Optimal attack window
        elif lap < 40:
            return 0.6  # High fuel, less degradation
        else:
            return 0.4  # Late race, DRS trains, settled pace
