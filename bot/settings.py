import os
import logging


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "generic": {
                "()": "logging.Formatter",
                "fmt": "[%(levelname)s] %(pathname)s:%(lineno)d - %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S]",
            },
        },
        "handlers": {
            "console": {
                "formatter": "generic",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": os.environ.get("LOG_LEVEL", "INFO"),
            "handlers": ["console"],
        },
    }
)

NAPCAT_API = os.environ["NAPCAT_API"]
