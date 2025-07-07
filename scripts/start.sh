#!/bin/bash

# Exit on any failure
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec gunicorn --bind 0.0.0.0:$PORT config.wsgi:application
