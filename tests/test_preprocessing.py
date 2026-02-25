"""Tests for preprocessing module."""

import numpy as np
import pandas as pd
import pytest

from src.preprocessing import (
    encode_categorical,
    handle_missing_values,
    remove_outliers,
    scale_features,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "age": [25.0, None, 35.0, 45.0, None, 55.0],
        "salary": [50000, 60000, None, 80000, 90000, 100000],
        "city": ["NYC", "LA", "NYC", "LA", "NYC", "LA"],
    })


@pytest.fixture
def numeric_df():
    return pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 100.0, 4.0, 5.0],  # 100 is an outlier
        "b": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
    })


class TestHandleMissingValues:
    def test_median_strategy(self, sample_df):
        result = handle_missing_values(sample_df, strategy="median")
        assert result["age"].isnull().sum() == 0
        assert result["salary"].isnull().sum() == 0

    def test_mean_strategy(self, sample_df):
        result = handle_missing_values(sample_df, strategy="mean")
        assert result.select_dtypes(include=[np.number]).isnull().sum().sum() == 0

    def test_constant_strategy(self, sample_df):
        result = handle_missing_values(sample_df, strategy="constant", fill_value=-1)
        assert (result["age"] == -1).sum() == 2

    def test_drop_strategy(self, sample_df):
        result = handle_missing_values(sample_df, strategy="drop")
        assert result.select_dtypes(include=[np.number]).isnull().sum().sum() == 0
        assert len(result) < len(sample_df)

    def test_invalid_strategy(self, sample_df):
        with pytest.raises(ValueError):
            handle_missing_values(sample_df, strategy="invalid")


class TestEncodeCategorical:
    def test_label_encoding(self, sample_df):
        result = encode_categorical(sample_df, columns=["city"], method="label")
        assert result["city"].dtype in [np.int64, np.int32, int]

    def test_onehot_encoding(self, sample_df):
        result = encode_categorical(sample_df, columns=["city"], method="onehot")
        assert "city" not in result.columns
        assert any("city_" in col for col in result.columns)

    def test_auto_detect_columns(self, sample_df):
        result = encode_categorical(sample_df, method="label")
        assert result["city"].dtype in [np.int64, np.int32, int]


class TestScaleFeatures:
    def test_scaling(self, numeric_df):
        result = scale_features(numeric_df)
        # Scaled columns should have approximately zero mean
        for col in result.columns:
            assert abs(result[col].mean()) < 1e-10


class TestRemoveOutliers:
    def test_removes_outliers(self, numeric_df):
        result = remove_outliers(numeric_df, n_std=2.0)
        assert len(result) < len(numeric_df)
        assert 100.0 not in result["a"].values
