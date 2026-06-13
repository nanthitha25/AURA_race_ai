import json

def get_racing_decision(input_data):
    """
    input_data expected dict:
    {
        "gap": 0.35,
        "mistake_probability": 0.72,
        "tire_advantage": 0.8,
        "driver_type": "aggressive"
    }
    """
    gap = input_data.get("gap", 1.0)
    mistake_prob = input_data.get("mistake_probability", 0.0)
    tire_adv = input_data.get("tire_advantage", 0.5)
    
    # Decision Engine Logic
    if mistake_prob > 0.7 and tire_adv > 0.5 and gap < 0.8:
        action = "ATTACK"
        reason = "Opponent braking instability detected, high mistake probability and favorable tires."
        confidence = 89
    elif gap < 0.5:
        action = "PRESSURE"
        reason = "Within striking distance. Apply pressure to force a mistake."
        confidence = 75
    else:
        action = "SAVE TYRES"
        reason = "Gap is too large or opponent is stable. Conserve tires for later."
        confidence = 95
        
    return {
        "action": action,
        "corner": "Turn 10", # Static for now
        "confidence": confidence,
        "reason": reason
    }

if __name__ == "__main__":
    # Test
    test_input = {
        "gap": 0.35,
        "mistake_probability": 0.72,
        "tire_advantage": 0.8,
        "driver_type": "aggressive"
    }
    decision = get_racing_decision(test_input)
    print(json.dumps(decision, indent=2))
