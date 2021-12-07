import os
import shutil
from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import file
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
        description = form.description.data
        profile_color = form.profile_color.data
        password = form.password.data

        images_dir = current_app.config['PROFILES_IMG_DIR']

        file1 = form.profile_picture.data
        profile_picture = None

        file2 = form.cover_photo.data
        cover_photo = None

        if file1:
            profile_picture = secure_filename(file1.filename)
            profile_picture_path = os.path.join(images_dir, profile_picture)
            file1.save(profile_picture_path)
        elif file1 is None:
            profile_picture = 'profile_default.png'

        if file2:
            cover_photo = secure_filename(file2.filename)
            cover_photo_path = os.path.join(images_dir, cover_photo)
            file2.save(cover_photo_path)
        elif file2 is None:
            cover_photo = 'cover_default.png'
        
        user = User.get_by_email(email)
        if user is not None:
            return redirect(url_for('auth.login'))
        else:
            user = User(name = name, email = email, description = description)
            user.profile_picture = url_for('static', filename=os.path.join('images/profiles/', profile_picture))
            user.cover_photo = url_for('static', filename=os.path.join('images/profiles/', cover_photo))
            user.profile_color = profile_color
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

@bp_auth.route('/delete/', methods = ['GET','POST'])
@login_required
def delete():
    user = User.query.filter_by(id=int(current_user.id)).delete()
    db.session.commit()
    return redirect(url_for('public.index'))