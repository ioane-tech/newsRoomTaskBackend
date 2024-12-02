from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_cors import CORS
from socketio_instance import socketio

#blueprints
from auth.routes import auth_bp
from websocket.handler import websocket_bp  
from blogs.routes import blogs_bp



app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, methods=["OPTIONS", "POST", "GET", "DELETE"])

socketio.init_app(app, cors_allowed_origins="http://localhost:3000")

load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)



# bluepirnts
app.register_blueprint(blogs_bp, url_prefix="/blogs")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(websocket_bp, url_prefix="/websocket")


if __name__ == "__main__":
    socketio.run(app, debug=True)