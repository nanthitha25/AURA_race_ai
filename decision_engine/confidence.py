def calculate_confidence(mistake_prob, gap, driver_style):
    """
    Calculates the confidence percentage of the recommendation.
    """
    base = 50.0
    
    # Mistake prob gives a large boost to confidence
    base += (mistake_prob * 30.0)
    
    # Being very close increases confidence in an action
    if gap < 0.5:
        base += 10.0
        
    # Driver style modifiers
    if driver_style.lower() == "aggressive":
        base += 5.0
        
    # Cap at 99
    return min(99.0, round(base, 1))
