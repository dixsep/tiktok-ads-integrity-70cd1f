# Model artifacts

`risk_model.pkl` is a serialized scikit-learn `LogisticRegression`.

For the MVP it is **seeded, not trained**: `model.py` fits on two synthetic
points to initialize sklearn's internals, then overwrites `coef_`/`intercept_`
with hand-chosen weights. This keeps the *service boundary* honest — the worker
loads a real pickled model and calls `predict_proba` — while deferring a real
training pipeline.

To swap in a trained model, drop a new `risk_model.pkl` here with the same
`FEATURE_ORDER`. No code changes.
