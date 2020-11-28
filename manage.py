import uuid
import datetime
import random
import time
import sys

from flask import render_template
from flask_script import Manager
from faker import Faker

from app import db, app
from app.models import User

manager = Manager(app)


def print_progress(iteration, total, prefix='', suffix='', decimals=1,
        bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in
                                  percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%',
            suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


@manager.command
def init_db():
    db.create_all()


@manager.command
def create_sample_data():
    size = 500
    try:
        size = input("Insert the data size you want to create.\n")
        size = int(size) if int(size) >= 5 else 5
    except Exception:
        pass

    start_time = time.time()
    sys.stdout.write('--- Starting the creation of sample data ---\n')
    faker = Faker('es_ES')

    # Create users
    sys.stdout.write('   - Creating users\n')
    print_progress(0, size - 1, prefix='   ', bar_length=50)
    for _ in range(size):
        print_progress(_, size - 1, prefix='   ', bar_length=50)
        profile = faker.profile()
        password = User.generate_hash('admin')
        random_number = str(random.randint(1, size))
        db.session.add(User(
            username=profile.get('username') + random_number,
            full_name=profile.get('name'),
            password=password,
            email=random_number + profile.get('mail')))
    db.session.commit()
if __name__ == '__main__':
    manager.run()
