import uuid
import datetime

from flask import render_template
from flask_restful import Resource, reqparse, marshal_with, marshal
from flask_jwt_extended import jwt_required
from flask_mail import Message as MailMessage

from app import db, mail
from app.models import User, TokenBlacklist
from app.utils import (current_user, str2bool, abort, valid_username,
    valid_email)
from app.fields import user_fields, string


user_parser_edit = reqparse.RequestParser()
user_parser_edit.add_argument('email', type=string(empty=False))
user_parser_edit.add_argument('username', type=string(empty=False, lower=True,
        strip=True))
user_parser_edit.add_argument('password', type=string(empty=False))
user_parser_edit.add_argument('password_confirmation',
    type=string(empty=False))
user_parser_edit.add_argument('full_name', type=string(empty=False))


user_parser = reqparse.RequestParser()
user_parser.add_argument('user', type=str)

password_recovery_parser = reqparse.RequestParser()
password_recovery_parser.add_argument('recovery_code',
    type=string(empty=False))
password_recovery_parser.add_argument('email', type=string(empty=False))
password_recovery_parser.add_argument('password', type=string(empty=False))
password_recovery_parser.add_argument('password_confirmation',
    type=string(empty=False))


class UserResource(Resource):

    decorators = [jwt_required]

    def get(self):
        args = user_parser.parse_args()
        user = current_user()
        if not args.user:
            users = User.query.all()
            return [get_user_fields(user=u, to_user=user) for u in users]
        query = User.query.filter_by(username=args.user)
        try:
            int(args.user)
            query = User.query.filter_by(id=args.user)
        except ValueError:
            pass
        return marshal(user, user_fields)


class MeResource(Resource):

    decorators = [jwt_required]

    def get(self):
        user = current_user()
        return get_user_fields(user, private=True, with_invite=True)

    def put(self):
        user = current_user()
        args = user_parser_edit.parse_args()
        allowed_fields = user_fields.keys()
        for key in args.keys():
            if key in allowed_fields:
                if key == 'username' and args[key] and User.query.filter_by(
                        username=args.username).first():
                    return abort(400, message='Username already taken')
                elif key == 'username' and args[key] and not valid_username(
                        args.username):
                    return abort(400, message='Username is not valid.')
                if key == 'email' and args[key] and not valid_email(args[key]):
                    return abort(400, message='Wrong email supplied')
                if args[key] or args[key] is not None:
                    setattr(user, key, args[key])
            if (key == 'password' and args.password
                    and args.password_confirmation and args.current_password):
                if args.password_confirmation != args.password:
                    return abort(400, message='Passwords don\'t match.')
                elif not User.verify_hash(
                     args.current_password, user.password):
                    return abort(400,
                        message='The current password is incorrect')
                user.password = User.generate_hash(args.password)
                tokens = TokenBlacklist.query.filter_by(
                    user_identity=str(user.id)).all()
                for token in tokens:
                    db.session.delete(token)
        db.session.commit()
        return marshal(user, user_fields)


class PasswordRecoverResource(Resource):

    def post(self):
        args = password_recovery_parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if not user:
            return abort(400, message='This user does does not exist.')
        user.recovery_code = uuid.uuid4().hex
        user.recovery_code_expiration = (
            datetime.datetime.now() + datetime.timedelta(hours=3))
        db.session.commit()
        with mail.connect() as conn:
            # Send Email
            msg = MailMessage("Deletos - Cambiar contraseña",
                sender=("Deletos", "beta@deletos.app"))
            msg.add_recipient(user.email)
            msg.html = render_template("email/pass_recovery.html",
                user=user)
            conn.send(msg)
        return {'success': 1}

    def put(self):
        args = password_recovery_parser.parse_args()
        user = User.query.filter_by(recovery_code=args.recovery_code).first()
        if not args.recovery_code or not user:
            return abort(400, message='Recovery code not valid')
        elif user and user.recovery_code_expiration < datetime.datetime.now():
            return abort(400, message='Recovery code expired')
        if not args.password or (
                args.password and args.password != args.password_confirmation):
            return abort(400, message='Passwords do not match')
        user.password = User.generate_hash(args.password)
        user.recovery_code = None
        user.recovery_code_expiration = None
        tokens = TokenBlacklist.query.filter_by(
            user_identity=str(user.id)).all()
        for token in tokens:
            db.session.delete(token)
        db.session.commit()
