.PHONY: test lint format notebook daily commit clean setup new-lesson

# === Setup ===
setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Setup complete. Run: source .venv/bin/activate"

# === Testing ===
test:
	pytest tests/ -v --tb=short --cov=src --cov-report=term-missing

test-quick:
	pytest tests/ -x -q

# === Code Quality ===
lint:
	flake8 src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/ notebooks/
	isort src/ tests/

# === Jupyter ===
notebook:
	jupyter lab

# === Learning ===
new-lesson:
	@read -p "Lesson number (e.g. 02): " num; \
	read -p "Lesson title (e.g. data visualization): " title; \
	python scripts/new_lesson.py $$num "$$title"

# === Daily Workflow ===
daily: test lint commit
	@echo "✅ Daily workflow complete!"

commit:
	git add -A
	git commit -m "daily: $$(date '+%Y-%m-%d %H:%M') updates" || echo "Nothing to commit"
	git push || echo "⚠️  Push failed — check remote setup"

# === Cleanup ===
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage htmlcov/ .pytest_cache/
	@echo "🧹 Cleaned up"
