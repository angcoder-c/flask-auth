import os
from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from app import db
from . import bp_auth
from .forms import RegisterForm, LoginForm
from app.models import User

@bp_auth.route('/register/', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        file1 = form.profile_picture.data
        profile_picture = None
        file2 = form.cover_photo.data
        cover_photo = None

        if file1:
            profile_picture = secure_filename(file1.filename)
            images_dir = current_app.config['PROFILES_IMG_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, profile_picture)
            file1.save(file_path)

        if file2:
            cover_photo = secure_filename(file2.filename)
            images_dir = current_app.config['PROFILES_IMG_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, cover_photo)
            file2.save(file_path)

        user = User.get_by_email(email)
        if user is not None:
            return redirect(url_for('auth.login'))
        else:
            user = User(name = name, email = email)
            user.profile_picture = profile_picture
            user.cover_photo = cover_photo
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)

            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.home')
            return redirect(next_page)
    return render_template('auth/register_from.html', form=form)

@bp_auth.route('/login/', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.home')
            return redirect(next_page)
        else:
            return redirect(url_for('auth.register'))
    return render_template('auth/login_form.html', form=form)

@bp_auth.route('/logout/', methods = ['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('public.index'))