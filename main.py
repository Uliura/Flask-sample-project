from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from app import create_app, db
from models import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('login.html')


@main.route('/profile')
@login_required
def profile():
    if current_user.active:
        user_list = User.query.all()
        return render_template('profile.html', data=enumerate(user_list, 1))
    else:
        flash('Your account is blocked!')
        return redirect(url_for('auth.login'))


app = create_app()
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True)
