"""A tiny logistic-regression risk model with a seeded artifact.

In production this is trained offline; here we ship a hand-seeded model so the
service boundary is real even without a training pipeline.
"""
import os
import pickle

import numpy as np
from sklearn.linear_model import LogisticRegression

ARTIFACT = os.path.join(os.path.dirname(__file__), "artifacts", "risk_model.pkl")

# Order matters: the scorer builds vectors in exactly this order.
FEATURE_ORDER = ["char_count", "exclaim_runs", "upper_ratio", "rule_score"]


def _seed_model() -> LogisticRegression:
    """Hand-seed weights so the artifact behaves sensibly without training."""
    model = LogisticRegression()
    # Fit on two synthetic points to populate the sklearn internals,
    # then overwrite the learned parameters with chosen weights.
    model.fit(np.array([[0, 0, 0, 0], [1, 1, 1, 1]]), np.array([0, 1]))
    model.coef_ = np.array([[0.002, 0.8, 1.5, 2.0]])
    model.intercept_ = np.array([-2.0])
    return model


def load_model() -> LogisticRegression:
    if os.path.exists(ARTIFACT):
        with open(ARTIFACT, "rb") as fh:
            return pickle.load(fh)
    model = _seed_model()
    os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
    with open(ARTIFACT, "wb") as fh:
        pickle.dump(model, fh)
    return model


def vectorize(features: dict, rule_score: float) -> np.ndarray:
    row = {**features, "rule_score": rule_score}
    return np.array([[float(row[name]) for name in FEATURE_ORDER]])
