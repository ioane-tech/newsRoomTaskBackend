from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_counts
from auth.utils import hash_password, check_password
from models.dynamodb import create_user, get_counts, increment_sign_in_count, get_user

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

    increment_sign_in_count(username)
    token = create_access_token(identity=username)
    return jsonify({"token": token}), 200

# personal count route
@auth_bp.route("/user_counts", methods=["GET"])
@jwt_required()
def userCounts():
    username = get_jwt_identity()
    user = get_user(username)

    if user:
        global_count = get_counts(username)
        
        #check if we have error from db
        if 'error' in global_count:
            return jsonify({"error": global_count['error']}), 500
        
        return jsonify({"data": global_count}), 200
    
    return jsonify({"message": "User not found"}), 404

# global count route
@auth_bp.route("/global_counts", methods=["GET"])
@jwt_required()
def globalCounts():
    global_count = get_counts('')

    if 'error' in global_count:
        return jsonify({"error": global_count['error']}), 500
        
    return jsonify({"data": global_count}), 200
