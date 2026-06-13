import pandas as pd
import numpy as np
import os

def augment_outcomes():
    path = "data/processed/race_outcome_dataset.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    np.random.seed(42)
    n_samples = 2000

    # lap,position,gap_ahead,gap_behind,tyre_age,pace_delta,pit_stops,weather
    data = {
        "lap": np.random.randint(10, 70, n_samples),
        "position": np.random.randint(1, 21, n_samples),
        "gap_ahead": np.random.uniform(0.1, 10.0, n_samples),
        "gap_behind": np.random.uniform(0.1, 10.0, n_samples),
        "tyre_age": np.random.randint(1, 30, n_samples),
        "pace_delta": np.random.uniform(-1.0, 1.0, n_samples),
        "pit_stops": np.random.randint(0, 3, n_samples),
        "weather": np.random.randint(0, 2, n_samples), # 0 = dry, 1 = wet
    }

    df = pd.DataFrame(data)

    # Calculate final position based on deterministic logic with noise
    final_positions = []
    for i, row in df.iterrows():
        pos = row["position"]
        # If pace is faster (negative delta), tend to gain positions
        if row["pace_delta"] < -0.3:
            pos -= np.random.randint(0, 3)
        elif row["pace_delta"] > 0.3:
            pos += np.random.randint(0, 3)
            
        # Tyre age penalty
        if row["tyre_age"] > 20:
            pos += 1
            
        # Bound between 1 and 20
        pos = max(1, min(20, pos))
        final_positions.append(pos)
        
    df['final_position'] = final_positions

    df.to_csv(path, index=False)
    print(f"Generated {n_samples} synthesized race outcomes for training.")

if __name__ == "__main__":
    augment_outcomes()
