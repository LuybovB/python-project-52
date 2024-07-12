### Hexlet tests and linter status:

[![Actions Status](https://github.com/LuybovB/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/LuybovB/python-project-52/actions)


### Описание:

Task Manager — это проект, разработанный на Python с использованием фреймворка Django, который представляет собой систему управления задачами. Он позволяет создавать задачи, назначать исполнителей и изменять статусы задач. Для работы с системой требуется регистрация и аутентификация.
Фронтенд реализован на стороне бэкенда с использованием фреймворка Bootstrap. Страницы генерируются с помощью шаблонизатора DjangoTemplates.


### Стек технологий:
* **Python** = "^3.10"
* **Django** = "4.2.13"
* **django-bootstrap5** = "23.4"
* **django-filter** = "24.2"
* **django-widget-tweaks** = "1.5.0"
* **psycopg2-binary** = "2.9.9"
* **requests** = "2.32.3"
* **beautifulsoup4** = "4.12.3"
* **gunicorn** = "21.2.0"
* **uvicorn** = "0.30.1"
* **whitenoise** = "5.3.0"
* **dj-database-url** = "2.2.0"
* **python-dotenv** = "1.0.1"
* **flake8** = "7.1.0"
* **asgiref** = "3.8.1"


### Установка:

git clone https://github.com/tmvfb/python-project-52.git
cd python-project-52.git
make install

### Настройки(переменные окружения):

Example .env file

* DATABASE_URL=your_database_connection_url
* SECRET_KEY=your_django_secret_key
* ROLLBAR=your_rollbar_access_token

### Демонтрация проекта:
https://python-project-52-rm4g.onrender.com/
