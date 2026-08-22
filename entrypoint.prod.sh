#!/bin/sh
set -e

MAX_RETRIES=${DB_MAX_RETRIES:-30}
RETRY_INTERVAL=${DB_RETRY_INTERVAL:-2}
RETRY_COUNT=0

echo "==> [START] Entrypoint script is running..."
echo "==> [WAIT] Waiting for database to be ready..."

until python3 -c '
import os, sys
import django
from django.db import connections
from django.db.utils import OperationalError
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "depo_crud.settings.production")
try:
    django.setup()
    connections["default"].cursor().execute("SELECT 1")
    sys.exit(0)
except Exception:
    sys.exit(1)
'; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
        echo "==> [ERROR] Maximum retries ($MAX_RETRIES) reached. Database is still not ready. Exiting."
        exit 1
    fi

    echo "==> [WAIT] Database not ready. Retrying in $RETRY_INTERVAL seconds... (Attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep "$RETRY_INTERVAL"
done

echo "==> [SUCCESS] Database is ready!"

echo "==> [MIGRATE] Running migrations..."
python manage.py migrate --noinput

echo "==> [SETUP] Ensuring an admin user exists..."
python3 -c '
import django
django.setup()
from django.contrib.auth import get_user_model
import sys
sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)
' || python manage.py createsuperuser --noinput --username admin@admin.com --email admin@admin.com

echo "==> [STATIC] Collecting static files..."
if [ ! -f "static/manifest.json" ]; then
    echo "==> [WARNING] static/manifest.json not found!"
fi
python manage.py collectstatic --noinput

echo "==> [SERVER] Starting Gunicorn..."
WORKERS=${GUNICORN_WORKERS:-3}

exec gunicorn depo_crud.wsgi:application --bind 0.0.0.0:8000 --workers "$WORKERS" --access-logfile - --error-logfile - --timeout 120 --graceful-timeout 30
