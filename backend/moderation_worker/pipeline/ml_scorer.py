"""Score features with the ML model, returning a probability in [0, 1]."""
from backend.ml_classifier.model import load_model, vectorize

_model = None


def ml_risk_score(features: dict, rule_score: float) -> float:
    global _model
    if _model is None:
        _model = load_model()  # loaded once, reused per process
    vector = vectorize(features, rule_score)
    # predict_proba returns [[p_safe, p_risky]]; we want p_risky.
    return float(_model.predict_proba(vector)[0][1])
