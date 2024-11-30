from flask import Blueprint

websocket_bp = Blueprint("websocket", __name__)

@websocket_bp.route("/", methods=["GET"])
def websocket_handler():
    return "WebSocket handler placeholder"