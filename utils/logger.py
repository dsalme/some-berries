import logging
import logging.config
from pythonjsonlogger import json
from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG
import copy
import sys

LOGGING_CONFIG = copy.deepcopy(UVICORN_LOGGING_CONFIG)

# json formatter config
json_formatter = {
    "()": json.JsonFormatter,
    "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s",
}

LOGGING_CONFIG["formatters"]["json"] = json_formatter

LOGGING_CONFIG["handlers"]["console"] = {
    "class": "logging.StreamHandler",
    "stream": sys.stdout,
    "formatter": "json",
}

for logger in LOGGING_CONFIG["loggers"].values():
    logger["handler"] = "console"
    logger["level"] = "INFO"

LOGGING_CONFIG["root"] = {
    "handlers": ["console"],
    "level": "INFO",
}

# logging config
logging.config.dictConfig(LOGGING_CONFIG)
