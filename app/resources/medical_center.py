from flask_restful import Resource, reqparse, marshal_with, marshal
from flask import jsonify
from flask_jwt_extended import jwt_required

from app.utils import get_ip_location
from app.fields import string, medical_center_fields
from app.models import MedicalCenter

from app import db

medical_center_parser = reqparse.RequestParser()
medical_center_parser.add_argument('location', type=string(empty=False))

medical_center_new_parser = reqparse.RequestParser()
medical_center_new_parser.add_argument('location', type=string(empty=False),
    required=True)
medical_center_new_parser.add_argument('name', type=string(empty=False),
    required=True)
medical_center_new_parser.add_argument('website', type=string(empty=False),
    required=True)
medical_center_new_parser.add_argument('contact_methods',
    type=string(empty=False),
    required=True)


class MedicalCenterResource(Resource):

    def get(self):
        args = medical_center_parser.parse_args()
        location = args.location if args.location else get_ip_location()
        centers = MedicalCenter.query.all()
        return jsonify(
            [marshal(mc, medical_center_fields) for mc in centers])

    @jwt_required
    def post(self):
        args = medical_center_new_parser.parse_args()
        db.session.add(MedicalCenter(
                location=args.location,
                name=args.name,
                website=args.website,
                contact_methods=args.contact_methods))
        db.session.commit()
        return jsonify({'success': 1})
