from flask import render_template
from flask_security import current_user, login_required
from flask_security.decorators import roles_accepted

# from flask_babelex import gettext as _

from covidcore.models import User
from covidcore import covidcore


@covidcore.route('/')
@covidcore.route('/index')
@login_required
def index():
    return render_template("index.html")


@covidcore.route('/admin')
@login_required
@roles_accepted('admin')
def admin():
    users = User.query.all()
    return render_template(
        "admin/index.html", users)
