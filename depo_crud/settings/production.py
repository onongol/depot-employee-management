import sentry_sdk
from csp.constants import NONCE, NONE, SELF
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

# 6. Cookies: HTTPS-only, and the __Secure- prefix enforces that browser-side
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = "__Secure-csrftoken"
# Safe here because every form uses {% csrf_token %}; no JS reads the cookie
CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = "__Secure-sessionid"

# 7. HTTPS: without the proxy header is_secure() is always False behind TLS
# termination, which would make the redirect below loop forever
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
# Platform health probes (Railway, Render, Fly, Heroku) hit this path over plain
# http and treat anything but a 200 - a redirect included - as a failed deploy
SECURE_REDIRECT_EXEMPT = [r"^health/$"]

# 8. HSTS. Hardcoded so raising it goes through review - browsers cache the
# value and it cannot be walked back. Ramp 60s -> six days -> a year, and keep
# the certificate valid: HSTS kills the "continue anyway" button.
SECURE_HSTS_SECONDS = 60
# Inert until then: no subdomains yet, preload needs submitting at hstspreload.org
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)

# 9. CSP. Report-only for now: violations land in the browser console and
# nothing breaks, so the policy can be tightened against real traffic before it
# is enforced. Switch the setting name to CONTENT_SECURITY_POLICY once quiet.
# The only inline script is the theme block in base.html, which carries a nonce.
CONTENT_SECURITY_POLICY_REPORT_ONLY = {
    "DIRECTIVES": {
        "default-src": [SELF],
        "script-src": [SELF, NONCE],
        # Third-party widgets (flatpickr, select2, unfold) inject style tags;
        # drop 'unsafe-inline' once the report log shows it is unused.
        "style-src": [SELF, "'unsafe-inline'"],
        "img-src": [SELF, "data:"],
        "font-src": [SELF, "data:"],
        "connect-src": [SELF],
        "form-action": [SELF],
        "base-uri": [SELF],
        "frame-ancestors": [NONE],
        "object-src": [NONE],
    },
}

# 10. Email: Django defaults to no timeout at all, so one hung SMTP connection
# would pin a gunicorn worker forever
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", default=5)

# 11. Middleware: django-axes requires its middleware to run last
MIDDLEWARE = MIDDLEWARE + [AXES_MIDDLEWARE_PATH]
assert MIDDLEWARE[-1] == AXES_MIDDLEWARE_PATH, "AxesMiddleware must be last"

# 12. django-vite: resolve built asset URLs via static/manifest.json
DJANGO_VITE = {
    "default": {"dev_mode": False},
}

# 13. Sentry: error monitoring. Inactive until SENTRY_DSN is set - lets the app
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
