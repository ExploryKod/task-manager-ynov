install:
	pip install -r requirements.txt

test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

coverage:
	pytest --cov=src --cov-report=html

clean:
	rm -rf .pytest_cache htmlcov __pycache__
	find . -type f -name '*.pyc' -delete

lint:
	python -m py_compile $(find src/ -name '*.py')

all: clean install lint test coverage 