from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError, \
    RevokedTokenError
from flask_jwt_extended.utils import RevokedTokenError as UtilsRevokedToken
from flask_jwt_extended.utils import ExpiredSignatureError
from werkzeug.exceptions import MethodNotAllowed, NotFound

from app import app


@app.errorhandler(NoAuthorizationError)
def handle_missing_authorization_error(err):
    response = {
            'success': 0,
            'error': {
                'message': 'Missing authorization header.',
            }}
    return jsonify(response), 401


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed_error(err):
    response = {
            'success': 0,
            'error': {
                'message': 'Method not allowed.',
            }}
    return jsonify(response), 401


@app.errorhandler(NotFound)
def handle_not_found(err):
    response = {
            'success': 0,
            'error': {
                'message': 'Resource not found.',
            }}
    return jsonify(response), 404


@app.errorhandler(RevokedTokenError)
@app.errorhandler(UtilsRevokedToken)
@app.errorhandler(ExpiredSignatureError)
def handle_revoked_token(err):
    response = {
            'success': 0,
            'error': {
                'message': 'The token you are sending is revoked or expired.',
            }}
    return jsonify(response), 403


@app.errorhandler(Exception)
def server_error_handler(error):
    message = {
            'success': 0,
            'error': {'message': 'Internal server error'},
            }
    if app.debug:
        message = {
                'success': 0,
                'error': {'message': error.args[0] if error.args else ''},
                }
    capture_exception(error)
    return jsonify(message), 500


@app.errorhandler(400)
def client_error_handler(error):
    response = {
            'success': 0,
            'error': {},
            }
    if hasattr(error, 'data'):
        for data in error.data:
            response['error'][data] = error.data[data]
    else:
        response['error'] = error.get_description()
    capture_exception(error)
    return jsonify(response), 400


class TokenNotFound(Exception):
    """
    Indicates that a token could not be found in the database
    """
    pass
