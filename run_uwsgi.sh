#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
# Must be done twice for dependencies
python manage.py bash scripts/import_database.sh
python manage.py bash scripts/import_database.sh
uwsgi uwsgi.ini
