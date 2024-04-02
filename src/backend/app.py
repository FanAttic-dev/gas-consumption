from flask import Flask
from flask_cors import CORS
from config import Config

from src.api import api
from src.database import db


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)
    
    Config.UPLOAD_PATH.mkdir(exist_ok=True, parents=True)
    cors = CORS(app)
    
    app.register_blueprint(api)
    
    db.init_app(app)
    
    return app

