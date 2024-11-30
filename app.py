from flask import Flask
from flask_jwt_extended import JWTManager
import os

from auth.routes import auth_bp
from websocket import websocket_bp


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(websocket_bp, url_prefix="/websocket")

if __name__ == "__main__":
    app.run(debug=True)