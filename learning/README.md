# Udemy Learning Workspace

Organize your course work here! Each lesson gets its own folder.

## Folder Structure

```
learning/
├── data/                  ← Drop CSV files from Udemy here
│   ├── housing.csv
│   └── titanic.csv
├── lesson_01_pandas/      ← One folder per lesson/topic
│   ├── lesson_01.py       ← Python script version
│   └── lesson_01.ipynb    ← Jupyter notebook version
├── lesson_02_visualization/
│   ├── lesson_02.py
│   └── lesson_02.ipynb
└── ...
```

## Quick Start

```bash
# Create a new lesson (from project root):
python scripts/new_lesson.py 03 "linear regression"
# Creates: learning/lesson_03_linear_regression/
#          with .py and .ipynb templates ready to go!
```

## Tips

- Put CSV files in `learning/data/` — they're tracked by git so you can commit daily
- Each lesson folder has both .py and .ipynb — use whichever the instructor uses
- Run your .py files: `python learning/lesson_01_pandas/lesson_01.py`
- Open .ipynb files in VS Code and run cells with Shift+Enter
