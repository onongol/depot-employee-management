#!/bin/sh
set -e

echo "Waiting for database to be ready..."

until python - <<'PY'
import os, sys
import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE','depo_crud.settings')
try:
    django.setup()
    connections['default'].cursor().execute('SELECT 1')
    print("Connection successful!")
    sys.exit(0)
except OperationalError as e:
    # Выводим реальную ошибку в логи Railway
    print(f"Database connection failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
PY
do
  echo "Retrying in 2 seconds..."
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
WORKERS=${GUNICORN_WORKERS:-3}
exec gunicorn depo_crud.wsgi:application --bind 0.0.0.0:8000 --workers $WORKERS --access-logfile - --error-logfile - --timeout 120 --graceful-timeout 30