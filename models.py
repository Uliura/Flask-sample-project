from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    signup_time = db.Column(db.String(100))
    last_login_time = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True, nullable=False)

