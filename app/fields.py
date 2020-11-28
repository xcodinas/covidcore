from functools import lru_cache
import re

from flask_restful import fields, marshal


def datetime_to_string(date):
    return date.strftime("%a, %d %b %Y %H:%M:%S -0000")


def string(max_length=None, min_length=None, empty=True, email=False,
        lower=False, demoji_length=False, strip=False):
    def validate(s):
        if not demoji_length and max_length and len(s) > max_length:
            raise ValueError(
                "The string length is too long, its limit is %s" % max_length)
        elif demoji_length and max_length and len(
                demoji_replace(s)) > max_length:
            raise ValueError(
                "The string length is too long, its limit is %s" % max_length)
        if not demoji_length and min_length and len(s) < min_length:
            raise ValueError(
                "The string length is too short, it must be at least %s " %
                min_length)
        elif demoji_length and min_length and len(
                demoji_replace(s)) < min_length:
            raise ValueError(
                "The string length is too short, it must be at least %s " %
                min_length)

        if not empty and not s:
            raise ValueError("Must not be empty string")
        if email and '@gmail.com' in s:
            s = s[:-10].replace('.', '') + '@gmail.com'
        if lower:
            s = s.lower()
        if strip:
            s = ''.join(s.strip().split())
        return s
    return validate


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'full_name': fields.String,
    'is_expert': fields.Boolean,
    'answer_rating': fields.Float,
}

medical_center_fields = {
    'location': fields.String,
    'name': fields.String,
    'website': fields.String,
    'contact_methods': fields.String,
}

answer_fields = {
    'answer': fields.String,
    'user': fields.Nested(user_fields),
    'average_rating': fields.Float,
}

question_fields = {
    'title': fields.String,
    'question': fields.String,
    'user': fields.Nested(user_fields),
    'answers': fields.List(fields.Nested(answer_fields)),
    'anon': fields.Boolean,
}
