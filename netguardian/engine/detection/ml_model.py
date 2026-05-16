import logging
import os

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "anomaly_model.pkl")


try:
    anomaly_model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    logger.warning("Model file %s missing, falling back to synthetic model", MODEL_PATH)
    anomaly_model = IsolationForest(contamination=0.05, random_state=42)
    anomaly_model.fit(np.random.randn(1000, 5) * 10 + 50)
