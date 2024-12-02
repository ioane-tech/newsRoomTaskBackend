from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from auth.utils import hash_password, check_password
from models.dynamodb import create_user, get_user

auth_bp = Blueprint("auth", __name__)

# registration route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if get_user(username):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = hash_password(password)
    userCreation = create_user(username, hashed_password)

    print(userCreation)
    if 'error' in userCreation:
        return jsonify({"message": userCreation["error"]}), 500
    return jsonify({"message": userCreation["message"]}), 201

# login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = get_user(username)
    if not user or not check_password(password, user["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify({"token": token}), 200

