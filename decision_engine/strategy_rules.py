def evaluate_strategy(data):
    """
    Evaluates hardcoded racing strategy rules.
    Input data dict expects:
    - gap (float)
    - mistake_probability (float 0-1)
    - drs (bool)
    - tire_advantage (float)
    - tire_temperature (float)
    """
    if data.get("tire_temperature", 90) > 100:
        return "SAVE_TIRES", "Tires are overheating. Must cool down."
        
    if data.get("gap", 1.0) < 0.8 and data.get("mistake_probability", 0.0) > 0.7 and data.get("drs", True):
        return "ATTACK", "Opponent under pressure with DRS available."
        
    if data.get("tire_advantage", 0) > 0.5:
        return "PRESSURE", "Better tire condition. Stay close to force error."
        
    return "DEFEND", "Maintain position and conserve energy."
