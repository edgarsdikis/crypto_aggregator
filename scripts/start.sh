#!/bin/bash

set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Celery worker in background..."
celery -A config worker -l INFO --detach

echo "Starting Celery beat in background..."
celery -A config beat -l INFO --detach

echo "Starting server..."
exec gunicorn --bind 0.0.0.0:$PORT config.wsgi:application
