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

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


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


User.register()
MedicalCenter.register()
