dev:
	poetry run python -m main

deploy:
	docker compose -f docker/docker-compose.yml --project-directory . up --build

migration: revision head

revision: 
	poetry run alembic revision --autogenerate -m "auto"

head:
	poetry run alembic upgrade head

