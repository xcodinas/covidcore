from functools import wraps

from flask_jwt_extended import jwt_required
from flask_restful import Resource
from app.utils import current_user, abort

from app.models import User


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user.is_admin:
            return abort(403, error="403 Forbidden")
        return func(*args, **kwargs)
    return wrapper


class AdminStatsResource(Resource):

    decorators = [jwt_required, admin_required]

    def get(self):
        return {
            'users': User.query.count(),
            }
