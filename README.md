# Pro ML Setup

A professional Machine Learning project template for daily development, testing, and GitHub commits.

## Project Structure

```
Pro ML Setup/
├── data/
│   ├── raw/              # Original CSV data (immutable)
│   ├── processed/        # Cleaned & transformed data
│   └── sample/           # Small sample datasets for testing
├── notebooks/            # Jupyter notebooks for exploration
├── src/
│   ├── __init__.py
│   ├── data_loader.py    # Data loading & validation
│   ├── preprocessing.py  # Feature engineering & cleaning
│   ├── model.py          # Model training & evaluation
│   └── utils.py          # Shared utilities
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_preprocessing.py
│   └── test_model.py
├── outputs/              # Model outputs, plots, reports
├── models/               # Saved model artifacts
├── requirements.txt
├── pyproject.toml
├── Makefile
├── .gitignore
└── README.md
```

## Quick Start

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
make test

# 4. Launch Jupyter
make notebook

# 5. Daily commit
make daily
```

## Daily Workflow

```bash
# Run all tests, then commit & push
make daily

# Or step by step:
make test          # Run pytest
make lint          # Check code quality
make commit        # Git add, commit, push
```

## Key Commands

| Command          | Description                        |
|------------------|------------------------------------|
| `make test`      | Run all tests with pytest          |
| `make notebook`  | Launch Jupyter Lab                 |
| `make lint`      | Run flake8 linter                  |
| `make format`    | Auto-format code with black        |
| `make daily`     | Test + lint + commit + push        |
| `make clean`     | Remove caches and temp files       |

## Adding New Data

1. Place raw CSV files in `data/raw/`
2. Create a loader function in `src/data_loader.py`
3. Add tests in `tests/test_data_loader.py`
4. Use notebooks for exploration

## License

MIT
