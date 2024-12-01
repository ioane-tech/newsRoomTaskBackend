from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_cors import CORS

from auth.routes import auth_bp
from websocket.handler import websocket_bp
from counts.routes import counts_bp



app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, methods=["OPTIONS", "POST", "GET"])

load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


# bluepirnts
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(counts_bp, url_prefix="/counts")
app.register_blueprint(websocket_bp, url_prefix="/websocket")

if __name__ == "__main__":
    app.run(debug=True)