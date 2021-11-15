from flask import render_template
from flask_login import current_user
from . import bp_public
from app.models import User

@bp_public.route('/')
@bp_public.route('/home/<string:name>/')
def index(name = None):
    context = {'name': name,
               'auth_user': current_user.is_authenticated,
               'users_list' : User.query.all()
    }
    return render_template('public/index.html', **context)

@bp_public.route('/<string:name>/')
def profile(name):
    return render_template('public/profile.html', user = User.query.filter_by(name=name).first())