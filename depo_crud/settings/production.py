import sentry_sdk
from django.core.exceptions import ImproperlyConfigured
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# 3. Debug Mode: True for development, False for production
DEBUG = False

# 4. Allowed Hosts: Domains your site can serve
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", cast=str.strip, default=[])
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS environment variable not set")
ALLOWED_HOSTS = ALLOWED_HOSTS + ["localhost", "127.0.0.1"]

# 5. CSRF Trusted Origins: Allowed origins for CSRF protection in production
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", cast=str.strip, default=[])
if not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured("CSRF_TRUSTED_ORIGINS environment variable not set")

# 6. Security Settings: Enforce secure cookies (HTTPS)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# __Secure- prefix backstops the *_SECURE flags above at the browser level.
CSRF_COOKIE_NAME = "__Secure-csrftoken"
SESSION_COOKIE_NAME = "__Secure-sessionid"

MIDDLEWARE = MIDDLEWARE + [AXES_MIDDLEWARE_PATH]
assert MIDDLEWARE[-1] == AXES_MIDDLEWARE_PATH, "AxesMiddleware must be last"

# django-vite: resolve built asset URLs via static/manifest.json.
DJANGO_VITE = {
    "default": {"dev_mode": False},
}

EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# Behind a proxy that terminates TLS, request.is_secure() is always False
# without these - breaks scheme detection in allauth's emails and absolute URLs.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# 7. Sentry: error monitoring. Inactive until SENTRY_DSN is set - lets the app
# run without it while the DSN is being provisioned.
SENTRY_DSN = env.str("SENTRY_DSN", default="")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=env.str("SENTRY_ENVIRONMENT", default="production"),
        send_default_pii=False,
        # .git isn't in the image, so auto-detection can't work; Railway sets
        # this automatically per deploy (needed for Sentry's GitHub release view).
        release=env.str("RAILWAY_GIT_COMMIT_SHA", default=None),
    )
