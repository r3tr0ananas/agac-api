build:
	pip install . -U

run:
	uvicorn app.main:app --reload --port 8083