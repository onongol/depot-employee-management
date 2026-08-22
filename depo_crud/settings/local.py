from shutil import which

from .base import *

# 3. Debug Mode: True for development, False for production
DEBUG = True

# 4. Allowed Hosts: Domains your site can serve
ALLOWED_HOSTS = ["*"]

# 5. CSRF Trusted Origins: Allowed origins for CSRF protection in production
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", cast=str.strip, default=[])

# 6. Security Settings: cookies don't need Secure over plain HTTP locally
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# 7. NPM Binary Path: Only needed in development for Unfold's asset management
NPM_BIN_PATH = env.str("NPM_BIN_PATH", default=None) or which("npm")
if not NPM_BIN_PATH:
    raise ValueError(
        "npm was not found. Set NPM_BIN_PATH in the environment or make npm available in PATH."
    )

# 8. Internal IPs: Used for debug toolbar and other development tools
INTERNAL_IPS = env.list("INTERNAL_IPS", cast=str.strip, default=["127.0.0.1", "::1"])

# 9. Application Definition
INSTALLED_APPS = [
    *INSTALLED_APPS,
    "whitenoise.runserver_nostatic",
    "debug_toolbar",
    "django_browser_reload",
]

# 10. Middleware: Hooks into Django's request/response process
MIDDLEWARE = [
    *MIDDLEWARE,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    AXES_MIDDLEWARE_PATH,
]
assert MIDDLEWARE[-1] == AXES_MIDDLEWARE_PATH, "AxesMiddleware must be last"

# Serve straight from STATICFILES_DIRS without requiring collectstatic first.
WHITENOISE_USE_FINDERS = True

# django-vite: proxy to the Vite dev server (npm run dev) for HMR.
DJANGO_VITE = {
    "default": {"dev_mode": True},
}

# EMAIL_BACKEND stays env-driven (not hardcoded): .env can still
# override it to real SMTP for testing allauth's email flow locally.
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
