from random import choice
from flask import render_template, redirect, url_for, current_app, Markup, escape
from flask_login import current_user, login_required
import random
import markdown
import os
import io
from . import bp_public
from app.models import User

@bp_public.route('/')
def index():
    context = {
        'registered_users' : len(User.query.all()),
        'current_user' : current_user
    }

    if current_user.is_authenticated:
        return redirect('home')

    return render_template('public/index.html', **context)

@bp_public.route('/home/', methods = ['GET','POST'])
@login_required
def home():

    users = User.query.all()
    recomendations = list()

    # 8 random users
    if len(users) >= 8:
        i = 0
        while i <= 8:
            rand_user = users[random.randint(0, len(users) -1)]
            if rand_user != current_user:
                recomendations.append(rand_user)
                i += 1
    else:
        recomendations = users
    
    context = {
        'current_user': current_user,
        'users' : users
    }
    return render_template('public/home.html', **context)

@bp_public.route('/tutorial/')
def tutorial():
    md_file = os.path.join(current_app.config['ROOT_DIR'], 'app/static/markdown/tutorial.md').replace('\\', '/')
    
    f = io.open(md_file, 'r', encoding='utf-8')
    md_tutorial = f.read()
    f.close()

    html_tutorial = Markup(markdown.markdown(md_tutorial,
                                    extensions = [
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc'
                                    ]))

    context = {
        'current_user': current_user,
        'tutorial' : html_tutorial,
        'escape': escape
    }
    return render_template('public/tutorial.html', **context)

@bp_public.route('/users/')
def users():
    context = {
        'current_user': current_user,
        'users' : User.query.all()
    }
    return render_template('public/users.html', **context)

@bp_public.route('/profile/<string:name>/')
def profile(name):
    user = User.query.filter_by(name=name).first()
    context = { 
        'user' : user,
        'current_user' : current_user
    }
    print(context['user'])
    return render_template('public/profile.html', **context)