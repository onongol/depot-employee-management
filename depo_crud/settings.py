import os
from pathlib import Path
from shutil import which

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from depo_crud import database_settings as database_config
from depo_crud import unfold_settings as unfold_config
from depo_crud.env_utils import get_env_list

load_dotenv()

# 1. Base Directory: The root of your project folder
BASE_DIR = Path(__file__).resolve().parent.parent


# 2. Security: Keep the secret key private in production
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable not set")


# 3. Debug Mode: True for development, False for production
DEBUG = os.getenv("DJANGO_DEBUG", "").strip().lower() in ("1", "true")


# 4. Allowed Hosts: Domains your site can serve
ALLOWED_HOSTS = ["*"] if DEBUG else get_env_list("ALLOWED_HOSTS", required=True)


# 5. CSRF Trusted Origins: Allowed origins for CSRF protection in production
CSRF_TRUSTED_ORIGINS = get_env_list("CSRF_TRUSTED_ORIGINS", required=not DEBUG)


# 6. Security Settings: Enforce secure cookies in production (HTTPS)
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG


# 7. NPM Binary Path: Only needed in development for Unfold's asset management
if DEBUG:
    NPM_BIN_PATH = os.getenv("NPM_BIN_PATH") or which("npm")
    if not NPM_BIN_PATH:
        raise ValueError(
            "npm was not found. Set NPM_BIN_PATH in the environment or make npm available in PATH."
        )


# 8. Internal IPs: Used for debug toolbar and other development tools
INTERNAL_IPS = get_env_list("INTERNAL_IPS", "127.0.0.1,::1")


# 9. Application Definition: List of enabled Django apps
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

# Application Definition plus if DEBUG
if DEBUG:
    INSTALLED_APPS += [
        "whitenoise.runserver_nostatic",
        "debug_toolbar",
        "django_browser_reload",
    ]


# 10. Middleware: Hooks into Django's request/response process
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

# Middleware plus if DEBUG
if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

# AxesMiddleware must be the last middleware in the list (django-axes requirement)
MIDDLEWARE += [
    "axes.middleware.AxesMiddleware",
]

# 11. URL Configuration: The root URL configuration for the project
ROOT_URLCONF = "depo_crud.urls"

# Required by django.contrib.sites (allauth dependency); single-site deployment.
SITE_ID = 1


# 12. Templates: Configuration for Django's template engine
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


# 13. WSGI Application: The WSGI entrypoint for the application callable for deployment
WSGI_APPLICATION = "depo_crud.wsgi.application"


# 14. Database: Database configuration
DATABASES = database_config.DATABASES


# 15. Password validation - Use Django's built-in validators for better security
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


# 16. Authentication: Redirect URLs for login/logout and default primary key field type
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# AxesStandaloneBackend must be first (django-axes requirement).
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# 17. Internationalization(i18n) and Timezone
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


# 18. Static files (CSS, JavaScript, Images)
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

# 19. Use BigAutoField for primary keys by default for better scalability
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# 20. Unfold custom Admin configuration
UNFOLD = unfold_config.UNFOLD


# 21. Email: SMTP configuration for registration confirmation emails.
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").strip().lower() in ("1", "true")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@example.com")


# 22. django-axes: locks out login attempts by username+IP after repeated failures
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hours
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_RESET_ON_SUCCESS = True
AXES_USERNAME_FORM_FIELD = "email"


# 23. django-allauth: email-only signup/login; HR-record matching lives in
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
# codes only - no WebAuthn/passkeys for now, no group is required to enable it.
MFA_SUPPORTED_TYPES = ["totp", "recovery_codes"]
MFA_TOTP_ISSUER = "Depot Management"
