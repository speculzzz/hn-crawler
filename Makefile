all: run

run:
	docker-compose up --build -d

down:
	docker-compose down

pytest:
	@pytest --cov=crawler tests/ -v

coverage:
	@pytest -s --cov --cov-report html --cov-fail-under 75

.PHONY: all run pytest coverage
