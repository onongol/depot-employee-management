import os

from depo_crud.env_utils import get_env_list

from .base import *

# 3. Debug Mode: True for development, False for production
DEBUG = False

# 4. Allowed Hosts: Domains your site can serve
ALLOWED_HOSTS = get_env_list("ALLOWED_HOSTS", required=True) + [
    "localhost",
    "127.0.0.1",
]

# 5. CSRF Trusted Origins: Allowed origins for CSRF protection in production
CSRF_TRUSTED_ORIGINS = get_env_list("CSRF_TRUSTED_ORIGINS", required=True)

# 6. Security Settings: Enforce secure cookies (HTTPS)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

MIDDLEWARE = MIDDLEWARE + [AXES_MIDDLEWARE_PATH]
assert MIDDLEWARE[-1] == AXES_MIDDLEWARE_PATH, "AxesMiddleware must be last"

# django-vite: resolve built asset URLs via static/manifest.json.
DJANGO_VITE = {
    "default": {"dev_mode": False},
}

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)

# Behind a proxy that terminates TLS, request.is_secure() is always False
# without these - breaks scheme detection in allauth's emails and absolute URLs.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
