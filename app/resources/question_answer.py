import datetime

from flask_restful import Resource, reqparse, marshal_with, marshal
from flask import jsonify
from flask_jwt_extended import jwt_required

from app.utils import (abort, needs_expert,
    current_user_or_none as current_user, str2bool)
from app.fields import string, question_fields
from app.models import CovidQuestion, CovidAnswer, AnswerRating

from app import db

question_new_parser = reqparse.RequestParser()
question_new_parser.add_argument('title', type=string(empty=False),
    required=True)
question_new_parser.add_argument('question', type=string(empty=False),
    required=True)
question_new_parser.add_argument('anon', type=str2bool)

answer_new_parser = reqparse.RequestParser()
answer_new_parser.add_argument('answer', type=string(empty=False),
    required=True)
answer_new_parser.add_argument('question', type=int, required=True)

delete_question_parser = reqparse.RequestParser()
delete_question_parser.add_argument('question', type=int, required=True)

delete_answer_parser = reqparse.RequestParser()
delete_answer_parser.add_argument('answer', type=int, required=True)

rating_parser = reqparse.RequestParser()
rating_parser.add_argument('rating', type=float, required=True)
rating_parser.add_argument('answer', type=int, required=True)


class QuestionResource(Resource):

    def get(self):
        questions = CovidQuestion.query.filter_by(
            deleted_at=None).order_by(CovidQuestion.created_at.desc()).all()
        return jsonify(
            [marshal(q, question_fields) for q in questions])

    def post(self):
        args = question_new_parser.parse_args()
        db.session.add(CovidQuestion(
                title=args.title,
                question=args.question,
                anon=args.anon,
                user=current_user() if not args.anon else None,
                ))
        db.session.commit()
        return jsonify({'success': 1})

    @jwt_required
    def delete(self):
        args = delete_question_parser.parse_args()
        question = CovidQuestion.query.filter_by(
            user=current_user()).filter_by(id=args.question).first()
        if question:
            question.deleted_at = datetime.datetime.now()
            db.session.commit()
            return jsonify({'success': 1})
        return jsonify({'success': 0})


class AnswerResource(Resource):

    @needs_expert
    def post(self):
        args = answer_new_parser.parse_args()
        question = CovidQuestion.query.filter_by(id=args.question).filter_by(
            deleted_at=None).first()
        if not question:
            abort(400, message='Wrong question or it has been deleted')
        db.session.add(CovidAnswer(
                answer=args.answer,
                question=question,
                user=current_user(),
                ))
        db.session.commit()
        return jsonify({'success': 1})

    @jwt_required
    def delete(self):
        args = delete_answer_parser.parse_args()
        answer = CovidAnswer.query.filter_by(
            user=current_user()).filter_by(id=args.answer).first()
        if answer:
            answer.deleted_at = datetime.datetime.now()
            db.session.commit()
            return jsonify({'success': 1})
        return jsonify({'success': 0})


class AnswerRatingResource(Resource):

    @jwt_required
    def post(self):
        args = rating_parser.parse_args()
        answer = CovidAnswer.query.filter_by(
            user=current_user()).filter_by(id=args.answer).first()
        rating = AnswerRating.query.filter_by(
                user=current_user()).filter_by(
                    answer=answer).first() if answer else None
        if answer and not rating:
            db.session.add(AnswerRating(
                    answer=answer,
                    rating=args.rating,
                    user=current_user()))
            db.session.commit()
            return jsonify({'success': 1, 'new_rating': answer.average_rating})
        elif answer and rating:
            rating.rating = args.rating
            db.session.commit()
            return jsonify({'success': 1, 'new_rating': answer.average_rating})
        return jsonify({'success': 0})
