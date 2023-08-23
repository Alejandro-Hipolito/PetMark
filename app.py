from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import secrets
from enum import Enum
import os


from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from flask_jwt_extended import JWTManager
from routes.auth import routes_auth


secret_key = secrets.token_hex(32)



app.register_blueprint(routes_auth, url_prefix='/api')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = secret_key


jwt = JWTManager(app)

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





# HERE START THE ROUTES




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

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     existing_user = User.query.filter_by(email = email).first()
#     if not existing_user or existing_user.password != password:
#         return jsonify({'msg' : 'Invalid credentials'})
    
#     return jsonify({'msg' : 'Login successful'}), 200

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     email = data.get("email")
#     password = data.get("password")
#     if not email or not password:
#         return jsonify({"message": "Error: email y contraseña requeridos"}), 400
#     user = User.query.filter_by(email=email, password=password).first()
#     if user is None:
#         return("El usuario no es correcto"), 400
#     token = create_access_token(identity=user.id)
#     print(token)
#     return jsonify({"token": token}), 200



     

@app.route('/user/<email>', methods=['GET'])
def get_user(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    user_data = {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "avatar": user.avatar,
        "role": user.role.value,
        "pets": [pet.name for pet in user.pets]
    }
    
    return jsonify(user_data), 200

@app.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    already_user = User.query.filter_by(email=email).first()
    if already_user:
        return jsonify({"msg" : "User already exists"}), 400

    signup = User(email=email, password=password)
    db.session.add(signup)
    db.session.commit()

    

    return jsonify({"msg" : "Signed up successfully!"}), 201

    


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port='4000', host="0.0.0.0")