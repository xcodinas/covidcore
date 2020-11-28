import json
import requests
import datetime
import re
from functools import wraps, lru_cache

from sqlalchemy.sql.expression import true
from sqlalchemy.sql import func
from sqlalchemy import cast
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, decode_token, \
    verify_jwt_in_request_optional
from flask_restful import marshal

from app import db, app, jwt, babel
from app.models import User, TokenBlacklist
from app.fields import user_fields
from app.exceptions import TokenNotFound

from config import Config

TAG_RE = re.compile(r'<[^>]+>')


def needs_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (request.headers.get('Authorization')
                and 'Bearer ' in request.headers.get('Authorization')
                and decode_token(
                    request.headers.get('Authorization')[7:]).get(
                    'type') == 'refresh'):
            return
        verify_jwt_in_request_optional()
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        if not current_user:
            return
        return func(current_user)
    return wrapper


def needs_expert(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (request.headers.get('Authorization')
                and 'Bearer ' in request.headers.get('Authorization')
                and decode_token(
                    request.headers.get('Authorization')[7:]).get(
                    'type') == 'refresh'):
            return
        verify_jwt_in_request_optional()
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        if not current_user.is_expert:
            return abort(422, message='Permissions needed')
        return func(*args, **kwargs)
    return wrapper


@needs_user
def update_last_request(user):
    user.last_request = datetime.datetime.now()


@app.before_request
def before_request():
    update_last_request()


@app.after_request
def after_request(response):
    try:
        save_user_ip()
    except Exception:
        pass

    # https://stackoverflow.com/questions/30241911/psycopg2-error-databaseerror-error-with-no-message-from-the-libpq
    db.engine.dispose()

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
        'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE')
    return response


def current_user():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        response = {
                'success': 0,
                'error': {
                    'message': 'Unknown user check that auth token is correct',
                }}
        return jsonify(response), 401
    return user


@lru_cache(99999)
def str2bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, int) and v == 1:
        return True
    elif isinstance(v, int) and v == 0:
        return False
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        return None


def filter_text(text):
    if text:
        return TAG_RE.sub('', text)


def valid_email(email):
    if re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*'
            + '(\.[a-z]{2,4})$', email) == None:
        return False
    return True


def valid_username(username):
    if re.match(
            '^[a-zA-Z0-9]+(?:[_ -]?[a-zA-Z0-9])*$', username) == None:
        return False
    return True


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    db_token = TokenBlacklist(
        jti=decoded_token['jti'],
        token_type=decoded_token['type'],
        user_identity=decoded_token[identity_claim],
        expires=datetime.datetime.fromtimestamp(decoded_token['exp']),
        revoked=False,
    )
    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    token = TokenBlacklist.query.filter_by(jti=jti).first()
    return token.revoked if token else True


def get_user_tokens(user_identity):
    """
    Returns all of the tokens, revoked and unrevoked, that are stored for the
    given user
    """
    return TokenBlacklist.query.filter_by(user_identity=user_identity).all()


def revoke_token(token_id, user):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    token = TokenBlacklist.query.filter_by(id=token_id,
        user_identity=str(user)).first()
    if not token:
        raise TokenNotFound("Could not find the token {}".format(token_id))
    token.revoked = True
    db.session.commit()


def unrevoke_token(token_id, user):
    """
    Unrevokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    token = TokenBlacklist.query.filter_by(id=token_id,
        user_identity=user).first()
    if not token:
        raise TokenNotFound("Could not find the token {}".format(token_id))
    token.revoked = False
    db.session.commit()


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


def unaccent_sql(column):
    return func.translate(column, 'áéíóúàèìòùäëïöüâêîôû',
        'aeiouaeiouaeiouaeiou')


def abort(code, json=False, *args, **kwargs):
    response = {
            'success': 0,
            'error': {}}
    response['error'] = kwargs
    return jsonify(response) if json else response, code


@babel.localeselector
def get_locale():
    user = current_user()
    if type(user) == User:
        return user.language


def get_ip_location():
    r = requests.get('https://freegeoip.app/json/{}'.format(
            request.remote_addr))
    j = json.loads(r.text)
    return j['city']
