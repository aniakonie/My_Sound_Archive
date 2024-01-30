from dotenv import load_dotenv
import os
from flask import Flask

load_dotenv()

def create_app():

    app = Flask(__name__)

    password_postgres = os.getenv("PASSWORD_POSTGRES")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{password_postgres}@localhost:5432/VMLdb"

    from website.database.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from .spotify_data.sp_auth import sp_auth
    from .library_views.library_views import library_views_bp
    from .general_views.general_views import general_views_bp

    app.register_blueprint(sp_auth, url_prefix='/sp_auth')
    app.register_blueprint(library_views_bp, url_prefix='/library')
    app.register_blueprint(general_views_bp, url_prefix='/')

    return app
