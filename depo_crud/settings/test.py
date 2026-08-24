from .production import *

# Fast hasher - tests don't need Argon2's cost factor.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Captures sent mail in django.core.mail.outbox instead of hitting real SMTP.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Insurance: the test client doesn't speak TLS, so this must stay False.
SECURE_SSL_REDIRECT = False
