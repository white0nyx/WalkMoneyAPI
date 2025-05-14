import json
import logging

json_formatter = logging.Formatter(
    json.dumps(
        {
            "time": "%(asctime)s",
            "level": "%(levelname)-6s",
            "loggerName": "%(name)s",
            "funcName": "%(funcName)s()",
            "line": "%(pathname)s:%(lineno)d",
            "message": "%(message)s",
        },
    )
)

ch = logging.StreamHandler()
ch.setFormatter(json_formatter)
