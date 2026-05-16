import os

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest


def generate_synthetic_normal(n_samples: int = 10000):
    return np.random.randn(n_samples, 5) * 10 + 50


def train_model(output_path: str = "ml/anomaly_model.pkl"):
    x_normal = generate_synthetic_normal()
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(x_normal)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    joblib.dump(model, output_path)
    print(f"Model saved as {output_path}")


if __name__ == "__main__":
    train_model()
