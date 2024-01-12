from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/VMLdb"
    db.init_app(app)

    from .sp_auth import sp_auth
    from .views import views
    from .home import home

    import website.database.models

    app.register_blueprint(sp_auth, url_prefix='/sp_auth')
    app.register_blueprint(views, url_prefix='/library')
    app.register_blueprint(home, url_prefix='/')

    return app
