import logging
import os
import sys
import time

from flask import request

loggers = {}
LOGGER_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'


def get_logger(name: str = "app", **kwargs):
    logger = loggers.get(name, None)

    if logger is None:
        logger = logging.getLogger(name)

        file_logger_path = kwargs.get("file_path", 'server.log')
        logger_level = kwargs.get("level", logging.INFO)
        logger_format = kwargs.get("format", LOGGER_FORMAT)
        logger_path_dir = os.path.dirname(file_logger_path)
        if len(logger_path_dir) > 0:
            os.makedirs(os.path.dirname(file_logger_path), exist_ok=True)

        logger.setLevel(logger_level)
        formatter = logging.Formatter(logger_format)
        fh = logging.FileHandler(file_logger_path, mode='w')
        sh = logging.StreamHandler(sys.stdout)

        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        logger.addHandler(fh)
        loggers[name] = logger

    return logger


def log_request(app, response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response

    timestamp = int(time.time())

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method),
        ('path', request.path),
        ('status', response.status_code),
        ('time', timestamp),
        ('ip', ip),
        ('host', host),
        ('params', args)
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id))

    parts = []
    for name, value in log_params:
        part = "{}={}".format(name, value)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)
