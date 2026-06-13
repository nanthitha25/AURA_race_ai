import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_outcome_model():
    print("Training Race Outcome Predictor Model...")
    path = "data/processed/race_outcome_dataset.csv"
    
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    data = pd.read_csv(path)

    features = [
        "lap", "position", "gap_ahead", "gap_behind", 
        "tyre_age", "pace_delta", "pit_stops", "weather"
    ]

    X = data[features]
    y = data["final_position"] - 1 # XGBoost expects 0-indexed classes (0 to 19 for P1 to P20)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Multi-class classification
    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        objective="multi:softprob",
        num_class=20,
        random_state=42
    )

    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, preds)}")

    os.makedirs("models/trained_models", exist_ok=True)
    joblib.dump(model, "models/trained_models/race_outcome.pkl")
    print("Race Predictor Trained and saved to models/trained_models/race_outcome.pkl")

class RaceOutcomePredictor:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "trained_models", "race_outcome.pkl")
        self.model = joblib.load(model_path)

    def predict(self, lap, position, gap_ahead, gap_behind, tyre_age, pace_delta, pit_stops, weather):
        df = pd.DataFrame([{
            "lap": lap,
            "position": position,
            "gap_ahead": gap_ahead,
            "gap_behind": gap_behind,
            "tyre_age": tyre_age,
            "pace_delta": pace_delta,
            "pit_stops": pit_stops,
            "weather": weather
        }])
        
        # Get probability array for all 20 positions
        probabilities = self.model.predict_proba(df)[0]
        
        # Return a dictionary mapped to actual position (1 to 20)
        outcomes = {f"P{i+1}": float(prob) for i, prob in enumerate(probabilities)}
        
        # Sort by highest probability
        sorted_outcomes = dict(sorted(outcomes.items(), key=lambda item: item[1], reverse=True))
        
        return sorted_outcomes

if __name__ == "__main__":
    train_outcome_model()
