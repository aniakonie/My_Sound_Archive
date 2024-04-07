from dotenv import load_dotenv
import os
from flask import Flask, render_template
from flask_migrate import Migrate

load_dotenv()

def page_not_found(e):
    return render_template("404.html"), 404

def unauthorized(e):
    return render_template("401.html"), 401


def create_app():

    app = Flask(__name__, static_url_path='')

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorized)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from website.database.models import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .spotify.views import spotify_bp
    from .library.views import library_bp
    from .home.views import home_bp
    from .library.demo import demo_bp

    app.register_blueprint(spotify_bp, url_prefix='/spotify')
    app.register_blueprint(library_bp, url_prefix='/library')
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(demo_bp, url_prefix='/demo')

    return app
