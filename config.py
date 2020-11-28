import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TABLES_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'es'
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    SECURITY_EMAIL_SENDER = ''
    SENTRY_CDN = os.environ.get('SENTRY_CDN') or None
