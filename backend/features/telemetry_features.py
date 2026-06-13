class TelemetryFeatureEngine:
    def extract(self, telemetry_slice):
        features = {}
        
        # Guard against empty slice
        if telemetry_slice.empty:
            return features
            
        features["avg_speed"] = float(telemetry_slice.Speed.mean())
        features["max_speed"] = float(telemetry_slice.Speed.max())
        features["brake_aggression"] = float(telemetry_slice.Brake.astype(float).mean())
        features["throttle_commitment"] = float(telemetry_slice.Throttle.mean())
        features["gear_changes"] = float(telemetry_slice.nGear.diff().abs().sum())
        
        return features
