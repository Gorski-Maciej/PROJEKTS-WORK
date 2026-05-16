import numpy as np

from detection.ml_model import anomaly_model


def test_model_prediction_shape_and_scores():
    n_features = getattr(anomaly_model, 'n_features_in_', 5)
    normal = np.random.randn(5, n_features) * 10 + 50
    scores = anomaly_model.decision_function(normal)
    assert len(scores) == 5
    assert np.isfinite(scores).all()
