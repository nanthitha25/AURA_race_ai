import os
import time
import json
import asyncio
import pyttsx3
import pandas as pd
import xgboost as xgb
import shap
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys

# Append parent dir so we can import decision_engine
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from decision_engine.decision_engine import get_racing_decision

app = FastAPI(title="AURA-Race AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TTS Engine safely
try:
    tts_engine = pyttsx3.init()
except Exception as e:
    tts_engine = None
    print(f"Warning: TTS initialization failed: {e}")

# Global state for ML model
xgb_model = None
explainer = None
feature_names = ["Gap", "Brake_Variation", "Steering_Error"]

def train_model():
    """Train a mock XGBoost model in memory for the API to use."""
    global xgb_model, explainer
    
    # Mock data as in mistake_prediction.py
    data = {
        "Gap": [0.4, 1.5, 0.3, 2.0, 0.2, 0.8, 0.35, 1.2, 0.25, 0.5],
        "Brake_Variation": [15, 2, 20, 5, 25, 8, 18, 4, 22, 10], 
        "Steering_Error": [20, 3, 25, 2, 30, 5, 12, 1, 15, 8],
        "Mistake": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    X = df[feature_names]
    y = df["Mistake"]

    xgb_model = xgb.XGBClassifier(
        n_estimators=50, learning_rate=0.1, max_depth=3,
        eval_metric='logloss', random_state=42
    )
    xgb_model.fit(X, y)
    
    # Initialize SHAP explainer
    explainer = shap.TreeExplainer(xgb_model)
    print("XGBoost Model & SHAP Explainer initialized.")

# Train on startup
@app.on_event("startup")
def startup_event():
    train_model()

class PredictRequest(BaseModel):
    gap: float
    brake_variation: float
    steering_error: float
    driver_type: str = "aggressive"
    tire_advantage: float = 0.8

@app.post("/predict")
def predict(req: PredictRequest):
    # Prepare input for ML
    input_df = pd.DataFrame({
        "Gap": [req.gap],
        "Brake_Variation": [req.brake_variation],
        "Steering_Error": [req.steering_error]
    })
    
    # Mistake Probability
    prob = float(xgb_model.predict_proba(input_df)[0][1])
    
    # SHAP Explanation
    shap_values = explainer.shap_values(input_df)
    # SHAP output logic can be complex depending on xgb version, fallback to a simple reason string
    # We will generate a mock explanation based on the input values
    reasons = []
    if req.brake_variation > 10:
        reasons.append(f"Opponent brake consistency reduced by {req.brake_variation}%")
    if req.gap < 0.5:
        reasons.append("Gap reduced below DRS range")
    reasons.append(f"Tire advantage +{req.tire_advantage * 100}%")

    # Decision Engine
    decision_input = {
        "gap": req.gap,
        "mistake_probability": prob,
        "tire_advantage": req.tire_advantage,
        "driver_type": req.driver_type
    }
    
    decision = get_racing_decision(decision_input)
    
    # Voice Alert if Attack
    if decision["action"] == "ATTACK" and tts_engine:
        text = f"Attack opportunity detected at {decision['corner']}. Confidence {decision['confidence']} percent."
        try:
            # We run TTS in a thread to not block async flow (or just fire and forget)
            # In a real app we'd queue this to a background worker
            tts_engine.say(text)
            tts_engine.runAndWait()
        except:
            pass

    return {
        "prediction": decision["action"],
        "mistake_probability": round(prob, 2),
        "confidence": decision["confidence"],
        "explanation": reasons,
        "engine_reasoning": decision["reason"]
    }

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Simulate an F1 telemetry stream
    gap = 1.0
    brake_var = 5.0
    steering_err = 5.0
    
    try:
        while True:
            # Random walk the gap and variation to simulate catching up
            gap -= 0.05
            brake_var += 0.5
            steering_err += 0.5
            
            if gap < 0.2:
                # Reset simulation loop
                gap = 1.5
                brake_var = 2.0
                steering_err = 2.0
                
            # Compute mistake probability live
            input_df = pd.DataFrame({"Gap": [gap], "Brake_Variation": [brake_var], "Steering_Error": [steering_err]})
            prob = float(xgb_model.predict_proba(input_df)[0][1])
            
            decision = get_racing_decision({
                "gap": gap,
                "mistake_probability": prob,
                "tire_advantage": 0.8,
                "driver_type": "aggressive"
            })

            data = {
                "gap": round(gap, 2),
                "brake_variation": round(brake_var, 2),
                "mistake_probability": round(prob * 100, 1),
                "action": decision["action"],
                "confidence": decision["confidence"]
            }
            
            await websocket.send_json(data)
            await asyncio.sleep(1.0) # 1Hz stream for UI clarity
    except Exception as e:
        print("WebSocket disconnected:", e)
