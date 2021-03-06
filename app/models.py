import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import event, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import aliased


from flask_babelex import gettext as _

from app import db


class TimestampsMixin(object):
    created_at = db.Column(db.DateTime,
        default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime,
        default=datetime.datetime.now())

    @staticmethod
    def create_time(mapper, connection, target):
        target.created_at = datetime.datetime.now()

    @staticmethod
    def update_time(mapper, connection, target):
        target.updated_at = datetime.datetime.now()

    @classmethod
    def register(cls):
        event.listen(cls, 'before_insert', cls.create_time)
        event.listen(cls, 'before_update', cls.update_time)


class User(db.Model, TimestampsMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    last_request = db.Column(db.DateTime, default=datetime.datetime.now())
    deleted_at = db.Column(db.DateTime)

    # Roles
    is_expert = db.Column(db.Boolean, default=False)

    questions = db.relationship("CovidQuestion", backref="user",
        lazy='dynamic')

    answers = db.relationship("CovidAnswer", backref="user",
        lazy='dynamic')

    answer_ratings = db.relationship("AnswerRating", backref="user",
        lazy='dynamic')

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @hybrid_property
    def answer_rating(self):
        rating = 0
        for answer in self.answers.all():
            if self.answer_ratings.count() > 0:
                rating += answer.average_rating
        return (rating / self.answers.count()) if rating else 0


class MedicalCenter(db.Model, TimestampsMixin):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    name = db.Column(db.String)
    website = db.Column(db.String)
    contact_methods = db.Column(db.String)


class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, nullable=False)
    token_type = db.Column(db.String, nullable=False)
    user_identity = db.Column(db.String, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }


class CovidQuestion(db.Model, TimestampsMixin):
    __tablename__ = 'covid_question'

    id = db.Column(db.Integer, primary_key=True)
    deleted_at = db.Column(db.DateTime)
    title = db.Column(db.String)
    question = db.Column(db.String)
    anon = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    answers = db.relationship('CovidAnswer',
        foreign_keys='CovidAnswer.question_id',
        primaryjoin='CovidAnswer.question_id == CovidQuestion.id',
        backref='question', lazy='dynamic')


class CovidAnswer(db.Model, TimestampsMixin):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question_id = db.Column(db.Integer, db.ForeignKey('covid_question.id'))
    ratings = db.relationship("AnswerRating", backref="answer",
        lazy='dynamic')

    @hybrid_property
    def average_rating(self):
        rating = 0
        for r in self.ratings.all():
            rating += r.rating
        return (rating / self.ratings.count()) if rating else 0


class AnswerRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    answer_id = db.Column(db.Integer, db.ForeignKey('covid_answer.id'))
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

User.register()
MedicalCenter.register()
