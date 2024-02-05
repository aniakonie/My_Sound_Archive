from dotenv import load_dotenv
import os
from flask import Flask
from flask_migrate import Migrate

load_dotenv()

def create_app():

    app = Flask(__name__)

    password_postgres = os.getenv('PASSWORD_POSTGRES')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{password_postgres}@localhost:5432/VMLdb"
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from website.database.models import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .spotify.sp_auth import sp_auth
    from .library_views.library_views import library_views_bp
    from .general_views.general_views import general_views_bp

    app.register_blueprint(sp_auth, url_prefix='/sp_auth')
    app.register_blueprint(library_views_bp, url_prefix='/library')
    app.register_blueprint(general_views_bp, url_prefix='/')

    return app
