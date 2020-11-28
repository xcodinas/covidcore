from werkzeug.exceptions import HTTPException

from flask import Flask
from flask_restful import Api as _Api
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_babelex import Babel

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from config import Config


class SQLAlchemy(_BaseSQLAlchemy):

    # https://github.com/pallets/flask-sqlalchemy/issues/589#issuecomment-361075700
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True


app = Flask(__name__, static_folder='static', static_url_path='')

chatbot = ChatBot("CovidBOT",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_url="sqlite:///database.sqlite3")


class Api(_Api):
    def error_router(self, original_handler, e):
        if self._has_fr_route() and isinstance(e, HTTPException):
            try:
                return self.handle_error(e)
            except Exception:
                pass
        return original_handler(e)

api = Api(app)
app.config.from_object(Config)
app.secret_key = b'_5#y2L148091"F4Q8z\n\xec]/'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask Mail
mail = Mail(app)

# Transaltions
babel = Babel(app)

jwt = JWTManager(app)


from app.resources.user import (
    UserResource, MeResource, PasswordRecoverResource)
from app.resources.medical_center import MedicalCenterResource
from app.resources.question_answer import (QuestionResource, AnswerResource,
    AnswerRatingResource)

# User
api.add_resource(UserResource, '/users')
api.add_resource(MeResource, '/users/me')
api.add_resource(PasswordRecoverResource,
    '/password_recover')

# Medical Centers
api.add_resource(MedicalCenterResource, '/medical_centers')

# Question Answer
api.add_resource(QuestionResource, '/questions')
api.add_resource(AnswerResource, '/questions/answers')
api.add_resource(AnswerRatingResource, '/questions/answers/rate')


from app import utils
from app import routes
from app import exceptions
assert routes
assert utils
assert exceptions
