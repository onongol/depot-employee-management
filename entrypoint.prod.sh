#!/bin/sh
set -e

echo "Waiting for database to be ready..."

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

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Ensuring admin user exists..."
python manage.py auto_admin --force

echo "Collecting static files..."
if [ ! -f "static/manifest.json" ]; then
    echo "WARNING: static/manifest.json not found!"
fi

python manage.py collectstatic --noinput

echo "Check collected static in /app/staticfiles:"
ls -la /app/staticfiles | head -n 10

echo "Starting Gunicorn server..."
exec gunicorn depo_crud.wsgi:application --bind 0.0.0.0:8000 --workers 3