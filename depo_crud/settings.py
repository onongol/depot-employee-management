"""
Django settings for project.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from pathlib import Path
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import sys
import platform


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable not set")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
DEBUG = os.getenv('DJANGO_DEBUG', '').strip().lower() in ('1', 'true')

# Currently empty. For production, add your domain or IP.
ALLOWED_HOSTS = [
    '.railway.app',
    '.example.com',
    #'www.zkhr_depo.com',
    
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://example.com',
]

# HTTPS
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

if DEBUG:
    ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'employee',
    'import_export', 
    'commando',
]

# Application definition DEBUG
if DEBUG:
    INSTALLED_APPS += [
        'whitenoise.runserver_nostatic',
        'debug_toolbar',
        'django_browser_reload',
    ]

# Path to the Node.js package manager (npm)
# NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
# Use env override or detect by platform (avoid hard-coded Windows path on Mac/CI)
NPM_BIN_PATH = os.getenv("NPM_BIN_PATH")
if not NPM_BIN_PATH:
    if platform.system() == "Windows":
        NPM_BIN_PATH = r"C:/Program Files/nodejs/npm.cmd"
    else:
        # common locations on macOS / Linux; prefer system npm in PATH
        NPM_BIN_PATH = "/usr/local/bin/npm"  # override with env if different

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django_browser_reload.middleware.BrowserReloadMiddleware',
    ]

ROOT_URLCONF = 'depo_crud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'employee.context_processors.global_departments', # Department context processor
                'employee.context_processors.is_employee',   # Check if user is an employee
                'employee.context_processors.is_master',    # Check if user is a master
                'employee.context_processors.is_payroll',  # Check if user is a payroll specialist
            ],
        },
    },
]

WSGI_APPLICATION = 'depo_crud.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Database
MYSQL_PUBLIC_URL = os.getenv('MYSQL_PUBLIC_URL')
if MYSQL_PUBLIC_URL:
    url = urlparse(MYSQL_PUBLIC_URL)
    DB_NAME = url.path.lstrip('/') 
    DB_USER = url.username
    DB_PASSWORD = url.password
    DB_HOST = url.hostname
    DB_PORT = url.port or 3306
else:
    DB_NAME = os.getenv('MYSQL_DATABASE') or os.getenv('MYSQLDATABASE')
    DB_USER = os.getenv('MYSQL_USER') or os.getenv('MYSQLUSER')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD') or os.getenv('MYSQLPASSWORD')
    DB_HOST = os.getenv('MYSQL_HOST') or os.getenv('MYSQLHOST', 'localhost')
    DB_PORT = int(os.getenv('MYSQL_PORT') or os.getenv('MYSQLPORT') or 3306)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

# Supported languages
LANGUAGES = [
    ('en', _('English')),
    ('mn', _('Mongolian')),
]

# Path to locale files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Ulaanbaatar'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory for collected static files

# Additional locations of static files
STATICFILES_DIRS = [BASE_DIR / "static",]

# Static files storage
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

INTERNAL_IPS = os.getenv('INTERNAL_IPS', '127.0.0.1').split(',')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login and logout redirect URLs
LOGIN_REDIRECT_URL = 'employee_list'
LOGOUT_REDIRECT_URL = 'home'

# Unfold settings
UNFOLD = {
    "SITE_TITLE": "Depot Management Admin",
    "SITE_HEADER": "Depot Management Admin",
    "SITE_ICON": lambda request: static("images/logo_light.svg"),

    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/x-icon",
            "href": lambda request: static("images/favicon.svg"),
        },
    ],
}

