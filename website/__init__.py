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
    migrate = Migrate(app, db)


    class User(db.Model):
        __tablename__ = "users"

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(30))
        account_created = db.Column(db.DateTime(timezone=True), default=func.now())
        user_music_platform = db.relationship('UserMusicPlatform')

        def __init__(self, email, password, account_created):
            self.email = email
            self.password = password
            self.account_created = account_created

        def __repr__(self):
            return f"<User id: {self.id}>"


    class UserMusicPlatform(db.Model):
        __tablename__ = "users_music_platform"

        id = db.Column(db.Integer, primary_key=True)
        music_platform_name = db.Column(db.String(15))
        music_platform_id = db.Column(db.String(15))
        access_token = db.Column(db.String(220))
        expires_in = db.Column(db.Integer)
        refresh_token = db.Column(db.String(131))
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

        def __init__(self, music_platform_name, music_platform_id, access_token, expires_in, refresh_token):
            self.music_platform_name = music_platform_name
            self.music_platform_id = music_platform_id
            self.access_token = access_token
            self.expires_in = expires_in
            self.refresh_token = refresh_token

        def __repr__(self):
            return f"<User of {self.music_platform_name}, music_platform_id: {self.music_platform_id}>"


    # from website.database.models import User, UserMusicPlatform

    from .sp_auth import sp_auth
    from .views import views
    from .home import home

    app.register_blueprint(sp_auth, url_prefix='/sp_auth')
    app.register_blueprint(views, url_prefix='/library')
    app.register_blueprint(home, url_prefix='/')

    return app
