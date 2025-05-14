.PHONY:

start:
	poetry run uvicorn \
		--reload \
		--host $$HOST \
		--port $$PORT \
		"$$APP_MODULE"

postgres_db:
	docker run --name=project_db \
	 			-e SSL_MODE='disable'\
				-e POSTGRES_USER=$$DB_USER\
				-e POSTGRES_PASSWORD=$$DB_PASS\
				-e POSTGRES_DB=$$DB_NAME\
				-e TZ=GMT-3\
				-p $$DB_PORT:5432 -d --rm postgres:alpine

revision:
	poetry run alembic revision --autogenerate -m init


migrate:
	poetry run alembic upgrade head