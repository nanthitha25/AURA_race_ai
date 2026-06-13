import joblib
import pandas as pd
import os

class AuraAIService:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "trained_models", "mistake_predictor.pkl")
        self.model = joblib.load(model_path)

    def predict_mistake(self, telemetry):
        # We need to map the telemetry dictionary to a DataFrame that matches the features the XGBoost model expects.
        data = pd.DataFrame([telemetry])
        
        # XGBoost output probability is [prob_0, prob_1]
        probability = self.model.predict_proba(data)[0][1]
        return probability

aura_ai = AuraAIService()
