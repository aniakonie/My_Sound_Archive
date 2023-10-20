from dotenv import load_dotenv
import os
from flask import Flask

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
    app.secret_key = os.getenv("SECRET_KEY")

    from .sp_auth import sp_auth

    app.register_blueprint(sp_auth, url_prefix='/')

    return app
