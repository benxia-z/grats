from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth import forms
from app.models import User
from app.quote import get_quote

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if not user.check_password(form.old_password.data):
            flash('Incorrect password, please try again.')
            return redirect(url_for('auth.change_password'))
        if user.check_password(form.new_password.data):
            flash('You already have this password, please try again.')
            return redirect(url_for('auth.change_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password successfully updated.')
        return redirect(url_for('main.user', username=current_user.username))
    return render_template('auth/change_password.html', title='Change Password',
                           form=form)
