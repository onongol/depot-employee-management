from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

if env.bool("DJANGO_READ_DOT_ENV_FILE", default=False):
    env.read_env(str(BASE_DIR / ".env"))

MYSQL_PUBLIC_URL = env.str("MYSQL_PUBLIC_URL", default=None)

if MYSQL_PUBLIC_URL:
    DATABASES = {"default": environ.Env.db_url_config(MYSQL_PUBLIC_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env.str("MYSQL_DATABASE", default=None)
            or env.str("MYSQLDATABASE", default=None),
            "USER": env.str("MYSQL_USER", default=None)
            or env.str("MYSQLUSER", default=None),
            "PASSWORD": env.str("MYSQL_PASSWORD", default=None)
            or env.str("MYSQLPASSWORD", default=None),
            "HOST": env.str("MYSQL_HOST", default=None)
            or env.str("MYSQLHOST", default="localhost"),
            "PORT": env.int("MYSQL_PORT", default=None)
            or env.int("MYSQLPORT", default=3306),
        }
    }

DATABASES["default"]["OPTIONS"] = {
    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
}

# Reuse connections across requests; set CONN_MAX_AGE=60 where the database is remote.
# Health checks are mandatory with it - the server drops idle
# connections, and Django would hand a dead one to the next request.
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=0)
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True
