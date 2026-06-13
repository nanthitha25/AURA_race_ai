import pandas as pd
import numpy as np
import os

def augment_overtakes():
    path = "data/processed/overtake_events.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    np.random.seed(42)
    n_samples = 1000

    data = {
        "driver": np.random.choice(["VER", "HAM", "NOR", "LEC", "SAI"], n_samples),
        "opponent": np.random.choice(["VER", "HAM", "NOR", "LEC", "SAI"], n_samples),
        "gap": np.random.uniform(0.1, 1.5, n_samples),
        "speed_delta": np.random.uniform(-5, 20, n_samples),
        "tyre_delta": np.random.randint(-10, 20, n_samples),
        "drs": np.random.randint(0, 2, n_samples),
        "opponent_weakness": np.random.uniform(0.1, 0.9, n_samples),
        "pressure_level": np.random.uniform(0.1, 0.9, n_samples),
        "corner_factor": np.random.uniform(0.1, 0.9, n_samples),
    }

    df = pd.DataFrame(data)

    # Synthesize realistic overtake success probability
    # Closer gap, higher speed delta, drs, and opponent weakness heavily influence success.
    prob = (
        (1.5 - df['gap']) * 0.2 +
        (df['speed_delta'] / 20) * 0.3 +
        (df['drs']) * 0.2 +
        (df['opponent_weakness']) * 0.15 +
        (df['corner_factor']) * 0.15
    )
    
    # Add noise and threshold to create binary target
    df['success'] = (prob + np.random.normal(0, 0.1, n_samples) > 0.65).astype(int)

    df.to_csv(path, index=False)
    print(f"Generated {n_samples} synthesized overtake events for training.")

if __name__ == "__main__":
    augment_overtakes()
