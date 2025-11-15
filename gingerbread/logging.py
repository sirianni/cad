from logging.config import dictConfig


def init():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[%(name)s] [%(levelname)-5s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stderr",
                }
            },
            "loggers": {
                "gingerbread": {
                    "level": "DEBUG",
                    "handlers": ["console"],
                    "propagate": False,
                }
            },
            "root": {
                "level": "ERROR",
                "handlers": ["console"],
            },
        }
    )
