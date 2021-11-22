from random import choice
from flask import render_template, redirect
from flask_login import current_user, login_required
import random
# from numpy import random
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

    users = User.query.all()

    # 8 random users
    recomendations = list()
    i = 0
    while i <= 8:
        rand_user = users[random.randint(0, len(users) -1)]
        if rand_user != current_user:
            recomendations.append(rand_user)
            i += 1
    
    context = {
        'current_user': current_user,
        'users' : list(set(recomendations))#list(set(random.choice(User.query.all(), 10)))
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