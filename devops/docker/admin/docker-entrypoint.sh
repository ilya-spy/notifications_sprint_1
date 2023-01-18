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
if [ ! -d "static" ]
then
  echo "Collecting static files"
  python manage.py collectstatic
else
  echo "Static files are already collected"
fi

# Start server
echo "Starting server"
gunicorn --bind :8000 --workers 1 config.wsgi:application
