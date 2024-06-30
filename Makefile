install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn -w 2 -b 0.0.0.0:8000 task_manager.wsgi

lint:
	poetry run flake8 task_manager

test:
	poetry run ./manage.py test

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage xml

check:
	poetry check

compilemessages:
	django-admin compilemessages

makemessages:
	django-admin makemessages --ignore="static" --ignore=".env" -l en

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate