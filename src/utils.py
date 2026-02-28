"""
Utility functions shared across the project.
"""

import time
from datetime import datetime
from functools import wraps
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"


def timer(func):
    """Decorator to time function execution."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱ {func.__name__} took {elapsed:.2f}s")
        return result

    return wrapper


def today_str() -> str:
    """Return today's date as YYYY-MM-DD string."""
    return datetime.now().strftime("%Y-%m-%d")


def save_plot(fig, name: str, fmt: str = "png") -> Path:
    """Save a matplotlib figure to outputs/."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUTS_DIR / f"{name}.{fmt}"
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    print(f"Plot saved to {filepath}")
    return filepath


def quick_eda(df: pd.DataFrame, title: str = "Dataset") -> None:
    """Print a quick exploratory data analysis summary."""
    print(f"\n{'='*50}")
    print(f"  EDA: {title}")
    print(f"{'='*50}")
    print(f"Shape: {df.shape}")
    print(f"\nColumn types:\n{df.dtypes.value_counts()}")
    print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nNumeric summary:\n{df.describe().round(2)}")


def plot_correlation_matrix(df: pd.DataFrame, title: str = "Correlation Matrix"):
    """Plot and return a correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include="number")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        ax=ax,
    )
    ax.set_title(title)
    plt.tight_layout()
    return fig
