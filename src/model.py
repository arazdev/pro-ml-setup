"""
Model Module
Train, evaluate, and save ML models.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"


CLASSIFIER_MAP = {
    "logistic_regression": LogisticRegression,
    "random_forest": RandomForestClassifier,
}

REGRESSOR_MAP = {
    "linear_regression": LinearRegression,
    "random_forest": RandomForestRegressor,
}


def train_classifier(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str = "random_forest",
    **kwargs,
) -> Any:
    """Train a classification model."""
    if model_name not in CLASSIFIER_MAP:
        raise ValueError(f"Unknown classifier: {model_name}. Choose from {list(CLASSIFIER_MAP)}")

    model_class = CLASSIFIER_MAP[model_name]
    model = model_class(**kwargs)
    model.fit(X_train, y_train)
    print(f"Trained {model_name} classifier on {X_train.shape[0]} samples")
    return model


def train_regressor(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str = "linear_regression",
    **kwargs,
) -> Any:
    """Train a regression model."""
    if model_name not in REGRESSOR_MAP:
        raise ValueError(f"Unknown regressor: {model_name}. Choose from {list(REGRESSOR_MAP)}")

    model_class = REGRESSOR_MAP[model_name]
    model = model_class(**kwargs)
    model.fit(X_train, y_train)
    print(f"Trained {model_name} regressor on {X_train.shape[0]} samples")
    return model


def evaluate_classifier(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Dict[str, Any]:
    """Evaluate a classification model and return metrics."""
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "report": classification_report(y_test, y_pred, output_dict=True),
    }
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    return metrics


def evaluate_regressor(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Dict[str, float]:
    """Evaluate a regression model and return metrics."""
    y_pred = model.predict(X_test)
    metrics = {
        "r2": float(r2_score(y_test, y_pred)),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
    }
    print(f"R²: {metrics['r2']:.4f} | MAE: {metrics['mae']:.4f} | RMSE: {metrics['rmse']:.4f}")
    return metrics


def save_model(model: Any, name: str) -> Path:
    """Save model to disk using joblib."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = MODELS_DIR / f"{name}.joblib"
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")
    return filepath


def load_model(name: str) -> Any:
    """Load a saved model from disk."""
    filepath = MODELS_DIR / f"{name}.joblib"
    if not filepath.exists():
        raise FileNotFoundError(f"Model not found: {filepath}")
    return joblib.load(filepath)


def save_metrics(metrics: dict, name: str) -> Path:
    """Save metrics as JSON."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUTS_DIR / f"{name}_metrics.json"
    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=2, default=str)
    print(f"Metrics saved to {filepath}")
    return filepath
