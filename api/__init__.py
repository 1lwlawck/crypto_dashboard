import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS
from api.routes import history_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(history_bp)

    return app
