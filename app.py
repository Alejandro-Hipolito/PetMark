from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
# db = SQLAlchemy(app)
# db.init_app(app) IN BIGGER PROJECTS



class User_role(Enum):
    COMMON_USER = 'common_user'
    ADMIN = 'admin'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    role = db.Column(db.Enum(User_role), nullable = False, default=User_role.COMMON_USER)

    pets = db.relationship('Pet', backref='user')


class Animal_Type(Enum):
    DOG = 'perro'
    CAT = 'gato'
    TURTLE = 'tortuga'
    BIRD = 'ave'
    OTHER = 'otro'

class Sex(Enum):
   MALE = 'macho'
   FEMALE = 'hembra' 

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True) 
    type = db.Column(db.Enum(Animal_Type), nullable=False, default=Animal_Type.DOG)
    sex = db.Column(db.Enum(Sex), nullable=True, default=Sex.MALE)
    age = db.Column(db.Integer, nullable=True)
    observations = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False) 
    description = db.Column(db.String(500), nullable=True)
    images = db.relationship('Image', backref='product')




class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200), db.ForeignKey('user.id'))
    product_id = db.Column(db.String(200), db.ForeignKey('product.id'))
    image = db.Column(db.String(200), nullable=False)


#Routes

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'avatar': user.avatar,
            'role': user.role.value
            })
    return jsonify(user_list)


if __name__ == '__main__':
    app.run()