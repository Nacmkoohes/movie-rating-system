import os
import logging
import logging.config


def setup_logging() -> None:


    level = os.getenv("LOG_LEVEL", "INFO").upper()

    config = {
        "version": 1,
        # keep other libraries' loggers working (uvicorn, sqlalchemy, ...)
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": level,
            }
        },
        # Root logger: everything that doesn't have its own config goes here
        "root": {
            "level": level,
            "handlers": ["console"],
        },
        #  if you want a dedicated logger name like doc examples: "movie_rating"
        "loggers": {
            "movie_rating": {
                "level": level,
                "handlers": ["console"],
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(config)
