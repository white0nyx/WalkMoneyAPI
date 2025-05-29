.PHONY:

start:
	uvicorn src.main:app --reload

postgres_db:
	docker run --name=project_db \
	 			-e SSL_MODE='disable'\
				-e POSTGRES_USER=$$DB_USER\
				-e POSTGRES_PASSWORD=$$DB_PASS\
				-e POSTGRES_DB=$$DB_NAME\
				-e TZ=GMT-3\
				-p $$DB_PORT:5432 -d --rm postgres:alpine

revision:
	alembic revision --autogenerate -m init


migrate:
	alembic upgrade head


db_insert:
	python3 data_insert/main_insert.py