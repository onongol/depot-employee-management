from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from depo_crud import database_settings as database_config
from depo_crud import unfold_settings as unfold_config

# 1. Base Directory: The root of your project folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

# Docker/CI inject real env vars; only bare local commands need .env.
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))


# 2. Security: Keep the secret key private in production
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="")
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY environment variable not set")


# 3. Application Definition: List of enabled Django apps
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
    "django_vite",
    "django.contrib.humanize",
    "django.contrib.sites",  # required by allauth
    "employee",
    "import_export",
    "commando",
    "simple_history",
    "axes",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.usersessions",
]


# 4. Middleware: Hooks into Django's request/response process
# Must stay last in MIDDLEWARE (django-axes requirement) - appended by
# each environment file, not here.
AXES_MIDDLEWARE_PATH = "axes.middleware.AxesMiddleware"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "allauth.usersessions.middleware.UserSessionsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "employee.middleware.user_context_cache.UserContextCacheMiddleware",  # Cache user settings for the request
]

# 5. URL Configuration: The root URL configuration for the project
ROOT_URLCONF = "depo_crud.urls"

# Required by django.contrib.sites (allauth dependency); single-site deployment.
SITE_ID = 1


# 6. Templates: Configuration for Django's template engine
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
                "employee.context_processors.user_roles",  # Check user roles
                "employee.context_processors.needs_department_warning",  # Department warning
                "employee.context_processors.navbar_page_types",  # Navbar page types
                "employee.context_processors.user_display_name",  # HR-record display name for the navbar menu
            ],
        },
    },
]


# 7. WSGI Application: The WSGI entrypoint for the application callable for deployment
WSGI_APPLICATION = "depo_crud.wsgi.application"


# 8. Database: Database configuration
DATABASES = database_config.DATABASES


# 9. Password validation - Use Django's built-in validators for better security
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

# Argon2id first (OWASP recommendation); old PBKDF2 hashes auto-upgrade on login.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password-reset link expiry, in seconds; also used by allauth's reset token generator.
PASSWORD_RESET_TIMEOUT = 60 * 60


# 10. Authentication: Redirect URLs for login/logout and default primary key field type
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# AxesStandaloneBackend must be first (django-axes requirement).
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# 11. Internationalization(i18n) and Timezone
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


# 12. Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Directory for collected static files

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Static files storage
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# django-vite: dev_mode is set per environment file below, not here - that's
# the whole point of this split (see local.py / production.py).
DJANGO_VITE = {
    "default": {},
}

# 13. Use BigAutoField for primary keys by default for better scalability
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# 14. Unfold custom Admin configuration
UNFOLD = unfold_config.UNFOLD


# 15. Email: SMTP configuration for registration confirmation emails.
EMAIL_HOST = env.str("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="no-reply@example.com")


# 16. django-axes: locks out login attempts by username+IP after repeated failures
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hours
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_RESET_ON_SUCCESS = True
AXES_USERNAME_FORM_FIELD = "email"


# 17. django-allauth: email-only signup/login; HR-record matching lives in
# employee/forms/allauth_forms.py, linking in employee/apps.py.
ACCOUNT_ADAPTER = "employee.adapters.CustomAccountAdapter"
ACCOUNT_FORMS = {
    "signup": "employee.forms.allauth_forms.CustomSignupForm",
    "login": "employee.forms.allauth_forms.CustomLoginForm",
    "reset_password_from_key": "employee.forms.allauth_forms.CustomResetPasswordKeyForm",
    "change_password": "employee.forms.allauth_forms.CustomChangePasswordForm",
    "reauthenticate": "employee.forms.allauth_forms.CustomReauthenticateForm",
}
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_RATE_LIMITS = {
    "signup": "5/h",
    "reset_password": "5/h",
}

# django-allauth: lets users see and sign out their other active sessions/devices.
USERSESSIONS_TRACK_ACTIVITY = True

# django-allauth: optional two-factor auth. TOTP (authenticator apps) + recovery
MFA_SUPPORTED_TYPES = ["totp", "recovery_codes"]
MFA_TOTP_ISSUER = "Depot Management"
