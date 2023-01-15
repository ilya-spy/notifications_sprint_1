#!/bin/bash

while ! nc -z ${POSTGRES_HOST} 5432; do
    sleep 2
    echo "still waiting for db ..."
done

echo "Postgres has been launched"

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Collect static files
echo "Collecting static files"
python manage.py collectstatic

# Start server
echo "Starting server"
gunicorn --bind :8000 --workers 1 config.wsgi:application
