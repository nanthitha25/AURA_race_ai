import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_overtake_model():
    print("Training Overtake Predictor Model...")
    path = "data/processed/overtake_events.csv"
    
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    data = pd.read_csv(path)

    features = [
        "gap", "speed_delta", "tyre_delta", "drs",
        "opponent_weakness", "pressure_level", "corner_factor"
    ]

    X = data[features]
    y = data["success"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, preds)}")
    print("\nClassification Report:\n", classification_report(y_test, preds))

    os.makedirs("models/trained_models", exist_ok=True)
    joblib.dump(model, "models/trained_models/overtake_predictor.pkl")
    print("Overtake Model Trained and saved to models/trained_models/overtake_predictor.pkl")

class OvertakePredictor:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "trained_models", "overtake_predictor.pkl")
        self.model = joblib.load(model_path)

    def predict(self, gap, speed_delta, tyre_delta, drs, opponent_weakness, pressure_level, corner_factor):
        df = pd.DataFrame([{
            "gap": gap,
            "speed_delta": speed_delta,
            "tyre_delta": tyre_delta,
            "drs": drs,
            "opponent_weakness": opponent_weakness,
            "pressure_level": pressure_level,
            "corner_factor": corner_factor
        }])
        probability = self.model.predict_proba(df)[0][1]
        return probability

if __name__ == "__main__":
    train_overtake_model()
