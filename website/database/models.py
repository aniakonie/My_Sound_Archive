from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    account_created = db.Column(db.DateTime(timezone=True), default=func.now())
    authenticated = db.Column(db.Boolean, default = False)
    user_music_platform = db.relationship('UserMusicPlatform')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True
    
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_anonymous(self):
        '''Anonymous users aren't supported.'''
        return False

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
