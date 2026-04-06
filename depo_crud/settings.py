import os
import platform
from pathlib import Path
from urllib.parse import urlparse

from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable not set")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "").strip().lower() in ("1", "true")

# Currently empty. For production, add your domain or IP.
ALLOWED_HOSTS = [
    ".railway.app",
    ".example.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://example.com",
]

# HTTPS
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

if DEBUG:
    ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "employee",
    "import_export",
    "commando",
    "simple_history",
]

# Application definition DEBUG
if DEBUG:
    INSTALLED_APPS += [
        "whitenoise.runserver_nostatic",
        "debug_toolbar",
        "django_browser_reload",
    ]

# Path to the Node.js package manager (npm)
# Use env override or detect by platform (avoid hard-coded Windows path on Mac/CI)
if DEBUG:
    NPM_BIN_PATH = os.getenv("NPM_BIN_PATH")
    if not NPM_BIN_PATH:
        if platform.system() == "Windows":
            NPM_BIN_PATH = r"C:/Program Files/nodejs/npm.cmd"
        else:
            NPM_BIN_PATH = "/usr/local/bin/npm"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = "depo_crud.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "employee.context_processors.global_departments",  # Department context processor
                "employee.context_processors.is_employee",  # Check if user is an employee
                "employee.context_processors.is_master",  # Check if user is a master
                "employee.context_processors.is_payroll",  # Check if user is a payroll specialist
                "employee.context_processors.needs_department_warning",  # Department warning
                "employee.context_processors.navbar_page_types",  # Navbar page types
            ],
        },
    },
]

WSGI_APPLICATION = "depo_crud.wsgi.application"

# Database
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

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en"

# Supported languages
LANGUAGES = [
    ("en", _("English")),
    ("mn", _("Mongolian")),
]

# Path to locale files
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

TIME_ZONE = "Asia/Ulaanbaatar"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Directory for collected static files

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Static files storage
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# INTERNAL_IPS:
# INTERNAL_IPS = os.getenv('INTERNAL_IPS', '127.0.0.1').split(',')
INTERNAL_IPS = [
    ip.strip()
    for ip in os.getenv("INTERNAL_IPS", "127.0.0.1,::1").split(",")
    if ip.strip()
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login and logout redirect URLs
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# Unfold settings
UNFOLD = {
    "SITE_TITLE": "Admin",
    "SITE_HEADER": "Admin",
    "SITE_ICON": {
        "light": lambda request: static("images/logo_light.svg"),
        "dark": lambda request: static("images/logo_dark.svg"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/x-icon",
            "href": lambda request: static("images/favicon.svg"),
        },
    ],
    "SHOW_LANGUAGES": True,
}
