#!/bin/sh
set -e

echo "Waiting for database to be ready..."

# MySQL client check
until python3 -c "
import os, sys, MySQLdb
try:
    conn = MySQLdb.connect(
        host=os.getenv('MYSQL_HOST', 'db'),
        user=os.getenv('MYSQL_USER'),
        passwd=os.getenv('MYSQL_PASSWORD'),
        db=os.getenv('MYSQL_DATABASE'),
        port=int(os.getenv('MYSQL_PORT', 3306))
    )
    conn.close()
except Exception as e:
    sys.exit(1)
" ; do
  echo "Database (MySQL) is unavailable - sleeping"
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
exec gunicorn depo_crud.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "$WORKERS" \
    --access-logfile - \
    --error-logfile - \
    --timeout 120 \
    --graceful-timeout 30
