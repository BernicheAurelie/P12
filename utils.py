from rest_framework.views import exception_handler
import logging


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        # response.data["message"] = "event creation impossible if contract not signed"
        return response


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s - level: %(levelname)s - message: %(message)s from: %(funcName)-8s - %(name)-8s",
                "datefmt": "%H:%M:%S",
            },
            "file": {
                "format": "%(asctime)s %(levelname)-8s - message: %(message)8s - from: %(funcName)-8s - (%(filename)-12s)",
                "datefmt": "%d-%b-%Y %H:%M:%S",
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "console"},
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "file",
                "filename": "./projet_12.log",
            },
        },
        "loggers": {"": {"level": "DEBUG", "handlers": ["console", "file"]}},
    }
)

logger = logging.getLogger(__name__)
