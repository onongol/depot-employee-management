#!/bin/sh

# exit on error
set -e

# Wait for the database to be ready
until python manage.py dbshell --command="SELECT 1;" 2>/dev/null; do
  echo "Waiting for database..."
  sleep 2
done

echo "Database is ready!"

# Apply migrations
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "Starting Gunicorn server..."
exec gunicorn depo_crud.wsgi:application --bind 0.0.0.0:8000 --workers 3
