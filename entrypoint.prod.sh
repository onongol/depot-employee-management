#!/bin/sh
set -e

# Wait for the database to be ready (Python-level check; no mysql client required)
until python - <<'PY'
import os, sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','depo_crud.settings')
django.setup()
from django.db import connections
try:
    connections['default'].cursor().execute('SELECT 1')
except Exception:
    sys.exit(1)
PY
do
  echo "Waiting for database..."
  sleep 2
done

echo "Database is ready!"

#echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating/ensuring admin user..."
python manage.py auto_admin --force

# Check built assets before collectstatic:
echo "Check built assets before collectstatic:"
ls -la static || true
ls -la static/dist || true
test -f static/dist/styles.css || echo "WARN: static/dist/styles.css not found"

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Check collected static files STATIC_ROOT (settings.py - /app/staticfiles)
echo "Check collected static:"
ls -la /app/staticfiles || true
ls -la /app/staticfiles/dist || true

echo "Starting Gunicorn server..."
exec gunicorn depo_crud.wsgi:application --bind 0.0.0.0:8000 --workers 3