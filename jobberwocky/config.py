import os
import logging

APP_NAME = 'jobberwocky'
APP_VERSION = '0.0.1'
APP_URL = os.environ.get('JOBBERWOCKY_APP_URL')

DATABASE_URL = os.environ.get('JOBBERWOCKY_DATABASE_URL')
EXTERNAL_API_URL = os.environ.get('JOBBERWOCKY_EXTRA_SOURCE_URL')

MAILGUN_DOMAIN = os.environ.get('JOBBERWOCKY_MAILGUN_DOMAIN')
MAILGUN_API_KEY = os.environ.get('JOBBERWOCKY_MAILGUN_API_KEY')

# ---------
# Log level
# ---------
LOG_LEVEL = os.environ.get('JOBBERWOCKY_LOG_LEVEL', 'INFO')
numeric_level = getattr(logging, LOG_LEVEL.upper(), None)

if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {log_level}")

logging.basicConfig(level=numeric_level)
