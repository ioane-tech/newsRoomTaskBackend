from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dynamodb import get_counts, get_user

counts_bp = Blueprint("counts", __name__)

# Personal count route
@counts_bp.route("/user_counts", methods=["GET"])
@jwt_required()
def userCounts():
    username = get_jwt_identity()
    user = get_user(username)

    if user:
        global_count = get_counts(username)
        
        # Check if there is an error from the DB
        if "error" in global_count:
            return jsonify({"message": global_count["error"]}), 500
        
        return jsonify({"data": global_count}), 200

    return jsonify({"message": "User not found"}), 404


# global count route
@counts_bp.route("/global_counts", methods=["GET"])
@jwt_required()
def globalCounts():
    global_count = get_counts('')

    if 'error' in global_count:
        return jsonify({"message": global_count['error']}), 500
        
    return jsonify({"data": global_count}), 200
