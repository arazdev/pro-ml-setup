"""
Preprocessing Module
Feature engineering, cleaning, and transformation utilities.
"""

from typing import List, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "median",
    fill_value: Optional[float] = None,
) -> pd.DataFrame:
    """Handle missing values in numeric columns.

    Args:
        df: Input DataFrame.
        strategy: 'mean', 'median', 'mode', 'drop', or 'constant'.
        fill_value: Value to use when strategy is 'constant'.
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if strategy == "drop":
        df = df.dropna(subset=numeric_cols)
    elif strategy == "constant":
        df[numeric_cols] = df[numeric_cols].fillna(fill_value or 0)
    elif strategy == "mean":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == "median":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == "mode":
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else 0)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return df


def encode_categorical(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: str = "label",
) -> pd.DataFrame:
    """Encode categorical columns.

    Args:
        df: Input DataFrame.
        columns: Columns to encode. If None, auto-detect object columns.
        method: 'label' or 'onehot'.
    """
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if method == "label":
        le = LabelEncoder()
        for col in columns:
            df[col] = le.fit_transform(df[col].astype(str))
    elif method == "onehot":
        df = pd.get_dummies(df, columns=columns, drop_first=True)
    else:
        raise ValueError(f"Unknown method: {method}")

    return df


def scale_features(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Standardize numeric features (zero mean, unit variance)."""
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def remove_outliers(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    n_std: float = 3.0,
) -> pd.DataFrame:
    """Remove rows with values beyond n standard deviations."""
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in columns:
        mean = df[col].mean()
        std = df[col].std()
        df = df[(df[col] - mean).abs() <= n_std * std]

    return df
