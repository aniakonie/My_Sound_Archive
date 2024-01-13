from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func

load_dotenv()

def create_app():

    app = Flask(__name__)

    password_postgres = os.getenv("PASSWORD_POSTGRES")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{password_postgres}@localhost:5432/VMLdb"

    db = SQLAlchemy(app)

    from .sp_auth import sp_auth
    from .views import views
    from .home import home

    app.register_blueprint(sp_auth, url_prefix='/sp_auth')
    app.register_blueprint(views, url_prefix='/library')
    app.register_blueprint(home, url_prefix='/')

    return app, db
