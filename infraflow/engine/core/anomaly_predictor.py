from __future__ import annotations

import logging
import os
import pickle
from typing import Any

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class AnomalyPredictor:
    """Predicts anomalies based on historical metrics."""

    def __init__(self, model_dir: str = '/app/models') -> None:
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.models: dict[str, IsolationForest] = {}
        self.scalers: dict[str, StandardScaler] = {}

    def _model_path(self, server_name: str) -> str:
        return os.path.join(self.model_dir, f'anomaly_{server_name}.pkl')

    async def train(self, db_pool: Any, server_name: str, hours: int = 168) -> bool:
        async with db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT time, metric_type, value
                FROM metrics
                WHERE server_name = $1
                  AND time > NOW() - $2::interval
                ORDER BY time
                """,
                server_name,
                f'{hours} hours',
            )

        if len(rows) < 100:
            logger.warning('Not enough data to train model for %s', server_name)
            return False

        grouped: dict[str, list[float]] = {'cpu': [], 'memory': [], 'disk': []}
        for row in rows:
            metric_type = row['metric_type']
            if metric_type in grouped:
                grouped[metric_type].append(float(row['value']))

        features: list[float] = []
        for metric_type in ('cpu', 'memory', 'disk'):
            values = grouped.get(metric_type, [])
            if len(values) >= 6:
                arr = np.array(values, dtype=float)
                features.extend([float(np.mean(arr)), float(np.std(arr))])
            else:
                features.extend([0.0, 0.0])

        X = np.array(features, dtype=float).reshape(1, -1)
        model = IsolationForest(contamination=0.05, random_state=42)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model.fit(X_scaled)

        with open(self._model_path(server_name), 'wb') as f:
            pickle.dump({'model': model, 'scaler': scaler}, f)

        self.models[server_name] = model
        self.scalers[server_name] = scaler
        return True

    def load(self, server_name: str) -> bool:
        path = self._model_path(server_name)
        if not os.path.exists(path):
            return False
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.models[server_name] = data['model']
        self.scalers[server_name] = data['scaler']
        return True

    def predict(self, server_name: str, recent_metrics: dict[str, list[float]]) -> tuple[bool, float]:
        if server_name not in self.models and not self.load(server_name):
            return False, 0.0

        features: list[float] = []
        for metric_type in ('cpu', 'memory', 'disk'):
            arr = recent_metrics.get(metric_type, [])
            if len(arr) >= 2:
                values = np.array(arr, dtype=float)
                features.extend([float(np.mean(values)), float(np.std(values))])
            else:
                features.extend([0.0, 0.0])

        X = np.array(features, dtype=float).reshape(1, -1)
        scaler = self.scalers[server_name]
        model = self.models[server_name]
        score = float(model.decision_function(scaler.transform(X))[0])
        return score < -0.1, score


predictor = AnomalyPredictor()
