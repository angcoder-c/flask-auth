from flask import render_template, redirect
from flask_login import current_user, login_required
from . import bp_public
from app.models import User

@bp_public.route('/')
def index():
    context = {
        'current_user' : current_user
    }

    if current_user.is_authenticated:
        return redirect('home')

    return render_template('public/index.html', **context)

@bp_public.route('/home/')
@login_required
def home():
    context = {
        'current_user': current_user
    }
    return render_template('public/home.html', **context)

@bp_public.route('/tutorial/')
def tutorial():
    context = {
        'current_user': current_user
    }
    return render_template('public/tutorial.html', **context)

@bp_public.route('/users/')
def users():
    context = {
        'current_user': current_user,
        'users_list' : User.query.all()
    }
    return render_template('public/users.html', **context)

@bp_public.route('/<string:name>/')
def profile(name):
    context = { 
        'user' : User.query.filter_by(name=name).first(),
        'current_user' : current_user
    }
    return render_template('public/profile.html', **context)