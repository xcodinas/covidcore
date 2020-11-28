import uuid
import datetime
import random
import time
import sys

from flask import render_template
from flask_script import Manager
from faker import Faker
from flask_mail import Message as MailMessage

from app import db, app, mail
from app.models import (User, Follow, Notification, NotificationType, Deleto,
    Message, Conversation, ConversationUser, UserLevel, BetaEmail, EmailDomain,
    Action)
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
def create_base_data():
    # Create notification types
    sys.stdout.write('   - Creating Notification Types\n')
    notification_types = [
        {
            'name': 'mention',
            'title': '@%(username)s has mentioned you.',
            'notification': '%(content)s'
        }, {
            'name': 'crush',
            'title': 'You and @%(username)s have a crush.',
            'notification': 'Break the ice!'
        }, {
            'name': 'redeleto',
            'title': '@%(username)s has redeleted your deleto',
            'notification': '%(content)s'
        }, {
            'name': 'dope',
            'title': '@%(username)s has doped your deleto',
            'notification': '%(content)s'
        }, {
            'name': 'follow',
            'title': '@%(username)s has started following you',
            'notification': 'Check out his profile!'
        }, {
            'name': 'reply',
            'title': '@%(username)s has replied to your deleto',
            'notification': '%(content)s'
        }, {
            'name': 'message',
            'title': 'Message from @%(username)s',
            'notification': '%(content)s'
        },
    ]

    actions = [
        {'name': 'redeleto',
            'exp': 8},
        {'name': 'dope',
            'exp': 4},
        {'name': 'reply',
            'exp': 6},
    ]

    print_progress(0, len(notification_types) - 1, prefix='   ', bar_length=50)
    for key, ntype in enumerate(notification_types):
        print_progress(key, len(notification_types) - 1, prefix='   ',
            bar_length=50)
        existing = NotificationType.query.filter_by(name=ntype['name']).first()
        if existing:
            existing.title = ntype['title']
            existing.notification = ntype['notification']
        else:
            db.session.add(NotificationType(name=ntype['name'],
                    notification=ntype['notification'],
                    title=ntype['title']))

    sys.stdout.write('   - Creating Some levels\n')
    for level in range(1, 101):
        existing = UserLevel.query.filter_by(level=level).count()
        if not existing and level != 1:
            exp_needed = (
                6 / 5 * level ** 3 - 15 * level ** 2 + 100 * level - 140)
            db.session.add(UserLevel(level=level, exp_needed=exp_needed))
        elif not existing and level == 1:
            db.session.add(UserLevel(level=1, exp_needed=0))
    db.session.commit()

    sys.stdout.write('   - Creating Email domains whitelist\n')
    with open('email_domains.txt') as email_whitelist:
        for domain in email_whitelist.readlines():
            domain = domain[:-1]
            existing = EmailDomain.query.filter_by(domain=domain).count()
            if not existing:
                db.session.add(EmailDomain(domain=domain))
    db.session.commit()

    sys.stdout.write('   - Creating Actions\n')
    print_progress(0, len(actions) - 1, prefix='   ', bar_length=50)
    for key, action in enumerate(actions):
        print_progress(key, len(actions) - 1, prefix='   ',
            bar_length=50)
        existing = Action.query.filter_by(name=action['name']).first()
        if not existing:
            db.session.add(Action(name=action['name'],
                    experience_given=action['exp']))
        else:
            existing.experience_given = action['exp']
    db.session.commit()

    sys.stdout.write('   - Adding missing invitation ocdes\n')
    users = User.query.filter_by(invitation_code=None).all()
    print_progress(0, len(actions) - 1, prefix='   ', bar_length=50)
    for key, user in enumerate(users):
        print_progress(key, len(users) - 1, prefix='   ',
            bar_length=50)
        invitation_code = uuid.uuid4().hex.upper()[:6]
        while User.query.filter_by(invitation_code=invitation_code).count():
            invitation_code = uuid.uuid4().hex.upper()[:6]
        user.invitation_code = invitation_code

    db.session.commit()


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
        password = User.generate_hash(
            faker.password(length=10, special_chars=True, digits=True,
            upper_case=True, lower_case=True))
        random_number = str(random.randint(1, size))
        db.session.add(User(
            username=profile.get('username') + random_number,
            full_name=profile.get('name'),
            password=password,
            gender=profile.get('sex'),
            birth_date=profile.get('birthdate'),
            location=profile.get('residence'),
            website=profile.get('website')[0],
            email=random_number + profile.get('mail')))
    db.session.commit()

    # Create Conversation
    sys.stdout.write('   - Creating Conversations\n')
    print_progress(0, size - 1, prefix='   ', bar_length=50)
    for user_id in range(size):
        conversation = Conversation()
        conversation.participants.append(ConversationUser(
                user_id=random.randint(1, size)))
        conversation.participants.append(ConversationUser(
                user_id=random.randint(1, size)))
        db.session.add(conversation)
        print_progress(_, size - 1, prefix='   ', bar_length=50)
    db.session.commit()

    sys.stdout.write('   - Creating Messages\n')
    print_progress(0, size - 1, prefix='   ', bar_length=50)
    for user_id in range(1, size):
        conversation_user = ConversationUser.query.filter_by(
            user_id=user_id).first()

        conversations = Conversation.query.filter(
            Conversation.participants.contains(conversation_user)).all()
        for conversation in conversations:
            for __ in range(random.randint(1, size)):
                db.session.add(Message(
                    text=faker.sentence(),
                    conversation_id=conversation.id,
                    user_id=user_id))
        print_progress(user_id, size - 1, prefix='   ', bar_length=50)
    db.session.commit()

    # Create follows
    sys.stdout.write('   - Creating Follows\n')
    print_progress(0, size - 1, prefix='   ', bar_length=50)
    for _ in range(size):
        print_progress(_, size - 1, prefix='   ', bar_length=50)
        from_user, to_user = random.sample(range(1, size), 2)
        follow = Follow.query.filter_by(from_user_id=from_user).filter_by(
            to_user_id=to_user).first()
        if not follow:
            db.session.add(Follow(from_user_id=from_user, to_user_id=to_user))
            ntype = NotificationType.query.filter_by(name='follow').first()
            db.session.add(Notification(
                    type=ntype, from_user_id=from_user, to_user_id=to_user))
    db.session.commit()

    # Create deletos
    sys.stdout.write('   - Creating Deletos\n')
    print_progress(0, size - 1, prefix='   ', bar_length=50)
    for user_id in range(1, size):
        for __ in range(random.randint(1, size)):
            db.session.add(Deleto(
                    text=faker.sentence(),
                    media=None,
                    media_type=None,
                    location="SRID=4326;POINT(%s %s)" % (
                        str(faker.longitude()),
                        str(faker.latitude())),
                    private=False,
                    user_id=user_id))
        print_progress(user_id, size - 1, prefix='   ', bar_length=50)
    db.session.commit()

    # TODO: Create threads
    # Dope and Redeleto some deletos
    # print('   - Making some dopes')
    # TODO: Add some dopes
    # print('   - Making some redeleto')
    # TODO: Add some redeletos

    sys.stdout.write('--- Sample data created correctly ---\n')
    sys.stdout.write("--- Execution time: %s seconds ---\n" % (
            time.time() - start_time))


@manager.command
def resend_confirmation_emails():
    unconfirmed_users = BetaEmail.query.filter_by(confirmed_at=None).all()
    with mail.connect() as conn:
        for user in unconfirmed_users:
            # Send Email
            msg = MailMessage("Beta - Validar Correo",
                sender=("Deletos", "beta@deletos.app"))
            msg.add_recipient(user.email)
            msg.html = render_template("email/beta_validation.html",
                user=user)
            conn.send(msg)


@manager.command
def send_beta_email():
    now = datetime.datetime.now().time()
    if now < datetime.time(7, 0) and now > datetime.time(23, 59):
        return
    confirmed_users = BetaEmail.query.filter(
        ~BetaEmail.confirmed_at.is_(None)).filter_by(
            beta_email_sent=False).order_by(
            BetaEmail.id.desc()).limit(30).all() or []
    with mail.connect() as conn:
        for user in confirmed_users:
            # Send Email
            msg = MailMessage("Deletos - ¡Bienvenidos a deletos!",
                sender=("Deletos", "beta@deletos.app"))
            msg.add_recipient(user.email)
            msg.html = render_template("email/beta.html",
                user=user)
            user.beta_email_sent = True
            conn.send(msg)
            db.session.commit()
if __name__ == '__main__':
    manager.run()
