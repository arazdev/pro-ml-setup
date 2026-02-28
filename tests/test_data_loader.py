"""Tests for data_loader module."""

import pandas as pd
import pytest

from src.data_loader import SAMPLE_DIR, load_csv, split_data, validate_dataframe

# ---- Fixtures ----


@pytest.fixture
def sample_df():
    """Create a simple sample DataFrame for testing."""
    return pd.DataFrame({
        "feature_1": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        "feature_2": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        "category": ["A", "B", "A", "B", "A", "B", "A", "B", "A", "B"],
        "target": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    })


@pytest.fixture
def df_with_nulls():
    """DataFrame with missing values."""
    return pd.DataFrame({
        "a": [1.0, None, 3.0, None, 5.0],
        "b": [10, 20, 30, 40, 50],
        "c": [None, None, None, None, 5.0],
    })


# ---- Tests ----

class TestLoadCSV:
    def test_load_sample_csv(self):
        """Test loading the sample CSV that ships with the project."""
        df = load_csv("iris_sample.csv", data_dir=str(SAMPLE_DIR))
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_load_missing_file_raises(self):
        """Test that loading a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_csv("nonexistent.csv")


class TestValidateDataframe:
    def test_valid_df(self, sample_df):
        report = validate_dataframe(sample_df)
        assert report["is_valid"] is True
        assert report["rows"] == 10
        assert report["columns"] == 4

    def test_missing_columns(self, sample_df):
        report = validate_dataframe(
            sample_df, required_columns=["feature_1", "missing_col"]
        )
        assert report["is_valid"] is False
        assert any(
            "Missing required columns" in issue for issue in report["issues"]
        )

    def test_high_null_pct(self, df_with_nulls):
        report = validate_dataframe(df_with_nulls, max_null_pct=0.3)
        assert report["is_valid"] is False
        assert any("null values" in issue for issue in report["issues"])


class TestSplitData:
    def test_split_shapes(self, sample_df):
        X_train, X_test, y_train, y_test = split_data(sample_df, target_column="target")
        assert len(X_train) + len(X_test) == len(sample_df)
        assert len(y_train) + len(y_test) == len(sample_df)
        assert "target" not in X_train.columns

    def test_split_ratio(self, sample_df):
        X_train, X_test, _, _ = split_data(
            sample_df, target_column="target", test_size=0.3
        )
        assert len(X_test) == 3  # 30% of 10
