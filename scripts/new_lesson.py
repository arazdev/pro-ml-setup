#!/usr/bin/env python3
"""
Create a new lesson folder with .py and .ipynb templates.

Usage:
    python scripts/new_lesson.py 02 "data visualization"
    python scripts/new_lesson.py 03 "linear regression"
    python scripts/new_lesson.py 15 "neural networks"

Creates:
    learning/lesson_02_data_visualization/
    ├── lesson_02.py
    └── lesson_02.ipynb
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEARNING_DIR = PROJECT_ROOT / "learning"


def create_lesson(number: str, title: str):
    # Build folder name
    slug = title.lower().replace(" ", "_").replace("-", "_")
    folder_name = f"lesson_{number}_{slug}"
    folder_path = LEARNING_DIR / folder_name

    if folder_path.exists():
        print(f"❌ Folder already exists: {folder_path}")
        sys.exit(1)

    folder_path.mkdir(parents=True)

    # --- Create .py file ---
    py_content = f'''"""
Lesson {number}: {title.title()}
{"=" * (len(title) + 12)}
Udemy Course - Follow along with the instructor

How to use:
  1. Put the CSV file from the lesson into: learning/data/
  2. Update the CSV filename below
  3. Run: python {folder_name}/lesson_{number}.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. LOAD YOUR CSV DATA
# ============================================================
# Change the filename to match your Udemy CSV file
CSV_FILE = "../data/your_file.csv"  # <- UPDATE THIS

# Uncomment when you have a CSV file:
# df = pd.read_csv(CSV_FILE)
# print(df.head())
# print(df.shape)
# print(df.info())

# ============================================================
# 2. FOLLOW ALONG — Write your code below
# ============================================================


print("Lesson {number}: {title.title()} — Ready to go!")


# ============================================================
# 3. YOUR PRACTICE / EXPERIMENTS
# ============================================================

'''

    py_path = folder_path / f"lesson_{number}.py"
    py_path.write_text(py_content)

    # --- Create .ipynb file ---
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# Lesson {number}: {title.title()}\\n",
                    "**Udemy Course** — Follow along with the instructor\\n",
                    "\\n",
                    "### How to use:\\n",
                    "1. Put the CSV file from the lesson into `learning/data/`\\n",
                    "2. Update the CSV filename in the cell below\\n",
                    "3. Run each cell with **Shift + Enter**"
                ],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Import libraries\\n",
                    "import pandas as pd\\n",
                    "import numpy as np\\n",
                    "import matplotlib.pyplot as plt\\n",
                    "import seaborn as sns\\n",
                    "\\n",
                    "%matplotlib inline\\n",
                    'sns.set_style("whitegrid")\\n',
                    'print("Libraries loaded!")'
                ],
                "execution_count": None,
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Load CSV Data\\n",
                    "Update the filename below to match your Udemy CSV file."
                ],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "outputs": [],
                "source": [
                    "# UPDATE THIS filename to your CSV file\\n",
                    'CSV_FILE = "../data/your_file.csv"  # <- CHANGE THIS\\n',
                    "\\n",
                    "# Uncomment these lines when you have your CSV:\\n",
                    "# df = pd.read_csv(CSV_FILE)\\n",
                    "# df.head()"
                ],
                "execution_count": None,
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Follow Along\\n",
                    "Type or paste code from the Udemy video in the cells below. ",
                    "Add new cells with the **+ Code** button or press **B**."
                ],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Your code here — follow along with the video:\\n",
                    ""
                ],
                "execution_count": None,
            },
            {
                "cell_type": "code",
                "metadata": {},
                "outputs": [],
                "source": [
                    "# More code here:\\n",
                    ""
                ],
                "execution_count": None,
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## My Notes\\n",
                    "Write your own notes, observations, or questions here."
                ],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    nb_path = folder_path / f"lesson_{number}.ipynb"
    nb_path.write_text(json.dumps(notebook, indent=1))

    print(f"✅ Created lesson {number}: {title.title()}")
    print(f"   📁 {folder_path.relative_to(PROJECT_ROOT)}/")
    print(f"   🐍 lesson_{number}.py")
    print(f"   📓 lesson_{number}.ipynb")
    print(f"\n   Next: drop your CSV into learning/data/ and start coding!")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/new_lesson.py <number> <title>")
        print('Example: python scripts/new_lesson.py 02 "data visualization"')
        sys.exit(1)

    num = sys.argv[1].zfill(2)
    title = " ".join(sys.argv[2:])
    create_lesson(num, title)
