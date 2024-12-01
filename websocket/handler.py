from flask import Blueprint
from flask_socketio import emit
from socketio_instance import socketio

socketio = socketio

websocket_bp = Blueprint("websocket", __name__)


@websocket_bp.route("/", methods=["GET"])
def websocket_handler():
    return "WebSocket handler placeholder"


def check_global_counts_length():
    from models.dynamodb import get_global_counts_length
    count = get_global_counts_length()
    if count == 5:
        socketio.emit('notification', {'message': 'Global count has reached 5!'})