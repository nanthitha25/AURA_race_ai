def process_telemetry(data):
    features = {
        "gap": data.get("gap", 0.5),
        "gap_closing_rate": 0.5,
        "brake_variation": abs(data.get("brake", 0) - 50),
        "throttle_variation": abs(data.get("throttle", 100) - 80),
        "speed_variation": data.get("speed", 300) / 10,
        "lap_time_loss": 0.2,
        "driver_aggression": 0.85,
        "driver_consistency": 0.90
    }
    return features
