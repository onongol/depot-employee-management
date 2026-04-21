done

#!/bin/sh
set -e

# ---------------------------------------------------------------------------
# Environment variable validation
# ---------------------------------------------------------------------------
echo "=== Database connection parameters ==="

MISSING_VARS=""

# Support both MYSQL_* and MYSQL* variable names, matching database_settings.py
DB_HOST="${MYSQL_HOST:-${MYSQLHOST:-}}"
DB_PORT="${MYSQL_PORT:-${MYSQLPORT:-3306}}"
DB_USER="${MYSQL_USER:-${MYSQLUSER:-}}"
DB_PASSWORD="${MYSQL_PASSWORD:-${MYSQLPASSWORD:-}}"
DB_NAME="${MYSQL_DATABASE:-${MYSQLDATABASE:-}}"

# MYSQL_PUBLIC_URL takes precedence in database_settings.py — skip individual
# var checks when it is present.
if [ -z "${MYSQL_PUBLIC_URL:-}" ]; then
    [ -z "$DB_HOST" ]     && MISSING_VARS="$MISSING_VARS MYSQLHOST"
    [ -z "$DB_USER" ]     && MISSING_VARS="$MISSING_VARS MYSQLUSER"
    [ -z "$DB_PASSWORD" ] && MISSING_VARS="$MISSING_VARS MYSQLPASSWORD"
    [ -z "$DB_NAME" ]     && MISSING_VARS="$MISSING_VARS MYSQLDATABASE"

    if [ -n "$MISSING_VARS" ]; then
        echo "ERROR: The following required environment variables are not set:$MISSING_VARS"
        echo "Set them in your Railway service variables and redeploy."
        exit 1
    fi

    echo "  Host     : $DB_HOST"
    echo "  Port     : $DB_PORT"
    echo "  User     : $DB_USER"
    echo "  Database : $DB_NAME"
    echo "  Password : (set, $(echo -n "$DB_PASSWORD" | wc -c) chars)"
else
    echo "  Using MYSQL_PUBLIC_URL (individual vars not required)"
fi

echo "======================================"

# ---------------------------------------------------------------------------
# Wait for the database with a retry limit
# ---------------------------------------------------------------------------
MAX_RETRIES=30
RETRY_INTERVAL=2
attempt=0

echo "Waiting for database to be ready..."

while [ $attempt -lt $MAX_RETRIES ]; do
    attempt=$((attempt + 1))
    echo "  Attempt $attempt/$MAX_RETRIES..."

    DB_READY=$(python - <<'PY'
import os, sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "depo_crud.settings")

try:
    django.setup()
    from django.db import connections
    conn = connections["default"]
    conn.ensure_connection()
    conn.cursor().execute("SELECT 1")
    print("ok")
except Exception as exc:
    # Print the full error so it appears in Railway's build/deploy logs
    print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
    sys.exit(1)
PY
    )

    if [ $? -eq 0 ] && [ "$DB_READY" = "ok" ]; then
        echo "Database is ready!"
        break
    fi

    if [ $attempt -ge $MAX_RETRIES ]; then
        echo "ERROR: Database did not become available after $((MAX_RETRIES * RETRY_INTERVAL)) seconds."
        echo "Check the error messages above for the root cause (e.g. wrong host, bad credentials, network issue)."
        exit 1
    fi

    sleep $RETRY_INTERVAL
done

# ---------------------------------------------------------------------------
# Migrations and startup
# ---------------------------------------------------------------------------
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