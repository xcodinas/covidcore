import os
basedir = os.path.abspath(os.path.dirname(__file__))

import datetime

from werkzeug.exceptions import MethodNotAllowed, BadRequest
from flask_jwt_extended.exceptions import NoAuthorizationError


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('COVIDCORE_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRATION_SECONDS = 3600
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=3)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=365)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_SECRET_KEY = 'deletos-api'
    JSON_SORT_KEYS = False
    BUNDLE_ERRORS = True
    SENTRY_CONFIG = {
        'ignore_exceptions': [
            MethodNotAllowed,
            NoAuthorizationError,
            BadRequest,
            ]
    }

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_SUPRESS_SEND = False
    MAIL_DEBUG = True
    BABEL_DEFAULT_LOCALE = 'es'
    DEBUG = os.environ.get('TEST_ENV')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
