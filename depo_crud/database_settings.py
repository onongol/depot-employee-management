import os
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

MYSQL_PUBLIC_URL = os.getenv("MYSQL_PUBLIC_URL")

if MYSQL_PUBLIC_URL:
    url = urlparse(MYSQL_PUBLIC_URL)
    DB_NAME = url.path.lstrip("/")
    DB_USER = url.username
    DB_PASSWORD = url.password
    DB_HOST = url.hostname
    DB_PORT = url.port or 3306
else:
    DB_NAME = os.getenv("MYSQL_DATABASE") or os.getenv("MYSQLDATABASE")
    DB_USER = os.getenv("MYSQL_USER") or os.getenv("MYSQLUSER")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQLPASSWORD")
    DB_HOST = os.getenv("MYSQL_HOST") or os.getenv("MYSQLHOST", "localhost")
    DB_PORT = int(os.getenv("MYSQL_PORT") or os.getenv("MYSQLPORT") or 3306)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
