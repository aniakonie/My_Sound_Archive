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

    from .sp_auth import sp_auth
    from .views import views
    from .home import home

    app.register_blueprint(sp_auth, url_prefix='/sp_auth')
    app.register_blueprint(views, url_prefix='/library')
    app.register_blueprint(home, url_prefix='/')

    return app
