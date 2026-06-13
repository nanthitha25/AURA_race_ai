def generate_radio_message(decision):
    action = decision.get("action")
    confidence = decision.get("confidence")
    overtake_prob = decision.get("overtake_probability", 0)
    expected_pos = decision.get("expected_position", 4)
    weakness = decision.get("weakness_detected", "General instability")
    futures = decision.get("evaluated_futures", [])
    
    message = f"AURA STRATEGY ANALYSIS: \n"
    message += f"Current P4. Evaluated {len(futures)} options. \n"
    
    if action == "ATTACK":
        message += f"Recommended: ATTACK. "
        message += f"Highest expected gain to P{expected_pos}. "
        message += f"Overtake Probability: {overtake_prob}%. "
    elif action == "PRESSURE":
        message += f"Recommended: PRESSURE. "
        message += f"Too risky to attack. Apply pressure. "
    elif action == "PIT":
        message += f"Recommended: PIT. Long term strategy. "
    else:
        message += f"Recommended: CONSERVE. "
        
    message += f"Confidence: {confidence}%"
    return message
