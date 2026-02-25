"""Tests for model module."""

import numpy as np
import pandas as pd
import pytest
from pathlib import Path

from src.model import (
    train_classifier,
    train_regressor,
    evaluate_classifier,
    evaluate_regressor,
    save_model,
    load_model,
    save_metrics,
)


@pytest.fixture
def classification_data():
    """Generate simple classification data."""
    np.random.seed(42)
    X = pd.DataFrame({
        "f1": np.random.randn(100),
        "f2": np.random.randn(100),
    })
    y = pd.Series((X["f1"] + X["f2"] > 0).astype(int), name="target")
    return X, y


@pytest.fixture
def regression_data():
    """Generate simple regression data."""
    np.random.seed(42)
    X = pd.DataFrame({
        "f1": np.random.randn(100),
        "f2": np.random.randn(100),
    })
    y = pd.Series(X["f1"] * 3 + X["f2"] * 2 + np.random.randn(100) * 0.1, name="target")
    return X, y


class TestClassifier:
    def test_train_logistic(self, classification_data):
        X, y = classification_data
        model = train_classifier(X, y, model_name="logistic_regression")
        assert hasattr(model, "predict")

    def test_train_random_forest(self, classification_data):
        X, y = classification_data
        model = train_classifier(X, y, model_name="random_forest", n_estimators=10)
        assert hasattr(model, "predict")

    def test_evaluate(self, classification_data):
        X, y = classification_data
        model = train_classifier(X, y, model_name="logistic_regression")
        metrics = evaluate_classifier(model, X, y)
        assert "accuracy" in metrics
        assert 0 <= metrics["accuracy"] <= 1

    def test_unknown_classifier(self, classification_data):
        X, y = classification_data
        with pytest.raises(ValueError):
            train_classifier(X, y, model_name="unknown_model")


class TestRegressor:
    def test_train_linear(self, regression_data):
        X, y = regression_data
        model = train_regressor(X, y, model_name="linear_regression")
        assert hasattr(model, "predict")

    def test_evaluate(self, regression_data):
        X, y = regression_data
        model = train_regressor(X, y, model_name="linear_regression")
        metrics = evaluate_regressor(model, X, y)
        assert "r2" in metrics
        assert "mae" in metrics
        assert "rmse" in metrics
        assert metrics["r2"] > 0.9  # Should fit well on this simple data


class TestModelIO:
    def test_save_and_load(self, classification_data, tmp_path, monkeypatch):
        X, y = classification_data
        model = train_classifier(X, y, model_name="logistic_regression")

        # Patch MODELS_DIR to use tmp_path
        monkeypatch.setattr("src.model.MODELS_DIR", tmp_path)
        save_model(model, "test_model")
        loaded = load_model("test_model")

        preds_original = model.predict(X)
        preds_loaded = loaded.predict(X)
        np.testing.assert_array_equal(preds_original, preds_loaded)

    def test_save_metrics(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.model.OUTPUTS_DIR", tmp_path)
        metrics = {"accuracy": 0.95, "f1": 0.93}
        path = save_metrics(metrics, "test")
        assert path.exists()
