from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app) IN BIGGER PROJECTS



class User_role(Enum):
    COMMON_USER = 'common_user'
    ADMIN = 'admin'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    role = db.Column(db.Enum(User_role), nullable = False, default=User_role.COMMON_USER)



class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = 



class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
