import datetime
import requests

from flask import jsonify, render_template, request
from flask_jwt_extended import (jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token, decode_token)
from flask_restful import reqparse, marshal

from app import app, db, chatbot
from app.exceptions import TokenNotFound
from app.models import User, TokenBlacklist
from app.fields import user_fields, string
from app.utils import (current_user, valid_email, get_user_tokens,
    add_token_to_database, revoke_token, unrevoke_token, unaccent_sql,
    str2bool, abort, valid_username, take)

from config import Config


register_parser = reqparse.RequestParser()
register_parser.add_argument('email', type=string(email=True, empty=False,
        strip=True),
    required=True, help="Email cannot be blank!")
register_parser.add_argument('username', type=string(empty=False, lower=True,
        strip=True),
    required=True, help="Username cannot be blank!")
register_parser.add_argument('password', type=string(empty=False, strip=True),
    required=True,
    help="Password cannot be blank!")
register_parser.add_argument('name', type=string(empty=False, strip=True),
    required=True,
    help="Name cannot be blank!")

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=string(empty=False, lower=True),
    required=True, help="Username cannot be blank!")
login_parser.add_argument('password', type=string(empty=False),
    required=True, help="Password cannot be blank!")

logout_parser = reqparse.RequestParser()
logout_parser.add_argument('push_token', type=string(empty=False),
     help="Push token cannot be blank")


@app.route('/')
def index():
    return {'ping': 'pong'}, 200


@app.route('/login', methods=['POST'])
def login():
    args = login_parser.parse_args()
    user = User.query.filter_by(username=args.username).first()
    if not user or not User.verify_hash(args.password, user.password):
        return abort(400, message="Bad username or password")

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify(
        user=marshal(user, user_fields),
        access_token=access_token,
        refresh_token=refresh_token), 200


@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    user = current_user()
    args = logout_parser.parse_args()
    # TODO: Delete auth token
    decoded_token = decode_token(request.headers.get('Authorization')[7:])
    token = TokenBlacklist.query.filter_by(jti=decoded_token['jti']).first()
    revoke_token(token.id, user.id)

    if token:
        db.session.delete(push_token)
        db.session.commit()
    return {'success': 1}, 200


@app.route('/register', methods=['POST'])
def register():
    args = register_parser.parse_args()
    if User.query.filter(User.username == args.username).count() != 0:
        return abort(400, message={'username': 'Username already registered'})
    elif User.query.filter(User.email == args.email).count() != 0:
        return abort(400, message={'email': 'Email already registered'})
    elif not valid_email(args.email):
        return abort(400, message={'email': 'This email is not valid'})
    elif not valid_username(args.username):
        return abort(400, message={'username': 'This username is not valid'})

    user = User(
        username=args.username,
        full_name=args.name,
        password=User.generate_hash(args.password),
        email=args.email)
    db.session.add(user)
    db.session.commit()
    return marshal(user, user_fields)


# Token stuff
@app.route('/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Do the same thing that we did in the login endpoint here
    user = current_user()
    access_token = create_access_token(identity=user.id)
    add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify({
        'access_token': access_token,
        'refresh_token': request.headers.get('Authorization')[7:]
        }), 201


# Provide a way for a user to look at their tokens
@app.route('/auth/token', methods=['GET'])
@jwt_required
def get_tokens():
    user = current_user()
    all_tokens = get_user_tokens(str(user.id))
    ret = [token.to_dict() for token in all_tokens]
    return jsonify(ret), 200


# Provide a way for a user to revoke/unrevoke their tokens
@app.route('/auth/token/<token_id>', methods=['PUT'])
@jwt_required
def modify_token(token_id):
    # Get and verify the desired revoked status from the body
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"msg": "Missing 'revoke' in body"}), 400
    revoke = json_data.get('revoke', None)
    if revoke is None:
        return jsonify({"msg": "Missing 'revoke' in body"}), 400
    if not isinstance(revoke, bool):
        return jsonify({"msg": "'revoke' must be a boolean"}), 400

    # Revoke or unrevoke the token based on what was passed to this function
    user = current_user()
    try:
        if revoke:
            revoke_token(token_id, user.id)
            return jsonify({'msg': 'Token revoked'}), 200
        else:
            unrevoke_token(token_id, user.id)
            return jsonify({'msg': 'Token unrevoked'}), 200
    except TokenNotFound:
        return jsonify({'msg': 'The specified token was not found'}), 404


@app.route('/chatbot', methods=['GET'])
def get_bot_response():
    text = request.args.get('message')
    if not text:
        return abort(400, message='Missing message parameter')
    return jsonify({'response': str(chatbot.get_response(text))})


@app.route('/news', methods=['GET'])
def get_news():
    return requests.get('https://newsapi.org/v2/%s?q=%s&language=%s&apiKey=%s'
        % ('top-headlines', 'covid-19', 'es',
            app.config['NEWS_API_KEY'])).json()


@app.route('/today', methods=['GET'])
def get_data():
    data = requests.get('https://api.covid19tracking.narrativa.com/api/%s'
        % datetime.date.today().strftime('%Y-%m-%d')).json()
    today_data = data['dates'][datetime.date.today().strftime('%Y-%m-%d')]
    top_regions = sorted(today_data['countries']['Spain']['regions'],
        key=lambda i: (i['today_confirmed']), reverse=True)
    # Top countries
    l = []
    for i in today_data['countries'].items():
        l.append(list(i)[1])
    top_countries = take(3, sorted(l,
        key=lambda i: (i['today_confirmed']), reverse=True))
    return jsonify({
            'last_updated': data['updated_at'],
            'spain': {
                'infected_today': today_data[
                    'countries']['Spain']['today_new_confirmed'],
                'total_cases': today_data[
                    'countries']['Spain']['today_confirmed'],
                'deceased_today': today_data[
                    'countries']['Spain']['today_new_deaths'],
                'deceased_total': today_data[
                    'countries']['Spain']['today_deaths'],
                'most_cases_comunities': [
                    {
                        'name': top_regions[0]['name'],
                        'cases': top_regions[0]['today_confirmed']
                    }, {
                        'name': top_regions[1]['name'],
                        'cases': top_regions[1]['today_confirmed']
                    }, {
                        'name': top_regions[2]['name'],
                        'cases': top_regions[2]['today_confirmed']
                    }]
                },
            'mr_worldwide': {
                'infected_active': data['total']['today_open_cases'],
                'total_cases': data['total']['today_confirmed'],
                'recovered': data['total']['today_recovered'],
                'deceased': data['total']['today_deaths'],
                'most_cases_countries': [
                    {
                        'name': top_countries[0]['name'],
                        'cases': top_countries[0]['today_confirmed']
                    }, {
                        'name': top_countries[1]['name'],
                        'cases': top_countries[1]['today_confirmed']
                    }, {
                        'name': top_countries[2]['name'],
                        'cases': top_countries[2]['today_confirmed']
                    }]
                }
            })
