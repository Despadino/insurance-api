dev: install
	poetry run python -m main

deploy: install
	docker compose -f docker/docker-compose.yml --project-directory . up --build

migration: revision head

revision:
	poetry run alembic revision --autogenerate -m "auto"

head:
	poetry run alembic upgrade head

install:
	poetry install --no-root