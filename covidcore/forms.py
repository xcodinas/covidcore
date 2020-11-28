from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField


class UserEditForm(FlaskForm):
    first_name = StringField('First Name', [])
    last_name = StringField('Last Name', [])
    phone = StringField('Phone number', [])
    street = StringField('Street', [])
    email = StringField('Email', [])
    city = StringField('City', [])
    country = StringField('Country', [])
    zip_code = IntegerField('Phone number', [])
    current_password = PasswordField('Password', [])
