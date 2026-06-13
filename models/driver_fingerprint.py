import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

def main():
    print("Training Driver Fingerprint Model (Personality DNA)...")
    
    # Load driver profiles
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "driver_profile.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run feature_engineering.py first.")
        return
        
    df = pd.read_csv(data_path)
    
    # Define personality classes: 0=Defensive, 1=Aggressive, 2=Balanced
    # We will generate labels based on a simple heuristic for our dummy dataset
    def assign_class(row):
        if row["Brake Aggression"] > 0.8 or row["Throttle"] > 0.9:
            return 1 # Aggressive
        elif row["Consistency"] > 0.9:
            return 2 # Balanced
        else:
            return 0 # Defensive

    df["Class"] = df.apply(assign_class, axis=1)
    
    # Prepare training data
    features = ["Brake Aggression", "Throttle", "Consistency", "Risk Index"]
    X_train = df[features]
    y_train = df["Class"]

    # Build and Train Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Model trained successfully.")

    # Test the model on the existing dataset
    predictions = model.predict(X_train)
    probabilities = model.predict_proba(X_train)
    
    class_names = {0: "Defensive Driver", 1: "Aggressive Driver", 2: "Balanced Driver"}
    
    print("\nDriver Fingerprint Results:")
    for idx, row in df.iterrows():
        driver = row["Driver"]
        pred_class = predictions[idx]
        conf_index = list(model.classes_).index(pred_class)
        conf = probabilities[idx][conf_index] * 100
        print(f"\nDriver: {driver}")
        print(f"Brake Aggression: {row['Brake Aggression']:.2f}, Throttle: {row['Throttle']:.2f}, Consistency: {row['Consistency']:.2f}")
        print(f"AI Prediction: {class_names[pred_class]}")
        print(f"Confidence: {conf:.1f}%")

if __name__ == "__main__":
    main()
