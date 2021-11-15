from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user

from app import db
from . import bp_auth
from .forms import RegisterForm, LoginForm
from app.models import User

@bp_auth.route('/register/', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index', name = current_user.name))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)
        if user is not None:
            return redirect(url_for('auth.login'))
        else:
            user = User(name = name, email = email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)

            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.index', name = user.name)
            return redirect(next_page)
    return render_template('auth/register_from.html', form=form)

@bp_auth.route('/login/', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index', name = current_user.name))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.index', name = user.name)
            return redirect(next_page)
        else:
            return redirect(url_for('auth.register'))
    return render_template('auth/login_form.html', form=form)

@bp_auth.route('/logout/', methods = ['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('public.index'))