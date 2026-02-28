"""
Data Loader Module
Load, validate, and split CSV datasets.
"""

from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLE_DIR = DATA_DIR / "sample"


def load_csv(filename: str, data_dir: Optional[str] = None) -> pd.DataFrame:
    """Load a CSV file from the given directory (default: data/raw/)."""
    if data_dir is None:
        filepath = RAW_DIR / filename
    else:
        filepath = Path(data_dir) / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath)
    print(f"Loaded {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Optional[list] = None,
    max_null_pct: float = 0.5,
) -> dict:
    """Validate a DataFrame and return a report dict."""
    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "null_counts": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "issues": [],
    }

    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            report["issues"].append(f"Missing required columns: {missing}")

    for col in df.columns:
        null_pct = df[col].isnull().mean()
        if null_pct > max_null_pct:
            report["issues"].append(
                f"Column '{col}' has {null_pct:.1%} null values "
                f"(threshold: {max_null_pct:.1%})"
            )

    report["is_valid"] = len(report["issues"]) == 0
    return report


def split_data(
    df: pd.DataFrame,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split DataFrame into train/test sets."""
    from sklearn.model_selection import train_test_split

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"Train: {X_train.shape[0]} rows | Test: {X_test.shape[0]} rows")
    return X_train, X_test, y_train, y_test
