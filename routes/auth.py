from flask import Blueprint, request, jsonify
from jwt import create_access_token
from app import User

routes_auth = Blueprint('routes_auth', __name__)


# @routes_auth.route("/login", method=['POST'])
# def login():
#     request.get_json()
#     if 

@routes_auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Error: email y contraseña requeridos"}), 400
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return("El usuario no es correcto"), 400
    token = create_access_token(identity=user.id)
    print(token)
    return jsonify({"token": token}), 200