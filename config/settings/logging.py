# Logging: send everything to the console - that's all PaaS platforms
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # keep Django's own loggers (django.request etc.) intact
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",  # keep SQL query logging out unless DEBUG is raised deliberately
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry_sdk": {
            "level": "ERROR",  # SDK's own diagnostic logging, not application logs
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
