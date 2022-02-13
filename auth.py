from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required
from app import db
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your password and try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=True)
        user.last_login_time = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first() \
                or User.query.filter_by(email=email).first():
            flash('Name or email already exists')
            return redirect(url_for('auth.signup'))
        new_user = User(username=username, email=email,
                        password=generate_password_hash(password,
                                                        method='sha256'),
                        signup_time=datetime.utcnow(),
                        last_login_time=datetime.utcnow())
        db.session.add(new_user)
        db.session.commit()
        login()
        return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        for user_id in request.form.getlist('id'):
            del_user = User.query.filter_by(id=user_id).first()
            db.session.delete(del_user)
            db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/block', methods=['GET', 'POST'])
@login_required
def block():
    for user_id in request.form.getlist('id'):
        block_user = User.query.filter_by(id=user_id).first()
        block_user.active = False
        db.session.add(block_user)
        db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/unblock', methods=['POST'])
@login_required
def unblock():
    for user_id in request.form.getlist('id'):
        unblock_user = User.query.filter_by(id=user_id).first()
        unblock_user.active = True
        db.session.add(unblock_user)
        db.session.commit()
    return redirect(url_for('main.profile'))
