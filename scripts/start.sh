#!/bin/bash

set -e

echo "Creating migrations..."
python manage.py makemigrations --noinput

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Ensuring superuser exists..."
python manage.py ensure_superuser  # Only creates if not local

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Celery worker in background..."
celery -A config worker -l INFO --detach

echo "Starting Celery beat in background..."
celery -A config beat -l INFO --detach

echo "Starting server..."
exec gunicorn --bind 0.0.0.0:$PORT config.wsgi:application
