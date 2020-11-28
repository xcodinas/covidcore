import datetime
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_security import Security
from flask_babelex import Babel
from flask_babelex import format_datetime as babel_datetime
from flask_mail import Mail

from config import Config


sentry_sdk.init(
    dsn=Config.SENTRY_CDN,
    integrations=[FlaskIntegration()],
)


covidcore = Flask(__name__)
covidcore.config.from_object(Config)
covidcore.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
covidcore.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
covidcore.config['SECURITY_PASSWORD_SALT'] = 'kfhasdgihwntlgy8f'
covidcore.config['SECURITY_RECOVERABLE'] = True

covidcore.jinja_env.globals.update(getattr=getattr)

# Flask Sqlalchemy
db = SQLAlchemy(covidcore)
# Flask Migrate
migrate = Migrate(covidcore, db)
# Flask security
login = LoginManager(covidcore)
login.login_view = 'login'
# Flask Babel
babel = Babel(covidcore)
# Falsk Mail
mail = Mail(covidcore)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['es', 'en'])

from covidcore import models, routes
assert models
assert routes

security = Security(covidcore, models.user_datastore)


@covidcore.template_filter('formatdatetime')
def format_datetime(value, format="yyyy-MM-dd H:mm"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    # Temporal fix of docker wrong time
    value = value + datetime.timedelta(hours=2)
    return babel_datetime(value, format)


def date_today(type=None):
    if type and type == 'datetime':
        return datetime.datetime.now()
    return datetime.date.today()

covidcore.jinja_env.globals.update(date_today=date_today)
covidcore.jinja_env.globals.update(len=len)
