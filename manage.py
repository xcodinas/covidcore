import os
import re

import datetime
from sqlalchemy.exc import IntegrityError

from flask_script import Manager
from flask_security.utils import hash_password

from covidcore import db, covidcore
from covidcore.models import user_datastore

manager = Manager(covidcore)


@manager.command
def init_db():
    db.create_all()


@manager.command
def create_user(
        email="admin@admin.com", name="admin", password="admin",
        role_name=None):
    user = user_datastore.create_user(
        email=email,
        first_name=name,
        password=hash_password(password),
        created_at=datetime.datetime.now(),
    )
    if role_name:
        role = user_datastore.find_or_create_role(name=role_name)
        user_datastore.add_role_to_user(user, role)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        print('That email is already in use.')
        return
    print('User created correctly. \nEmail: %s\n Role: %s' % (
            email, role_name or 'No role'))
    return user


if __name__ == '__main__':
    manager.run()
