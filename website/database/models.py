from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
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
    password = db.Column(db.String(60))
    account_created = db.Column(db.DateTime(timezone=True), default=func.now())
    authenticated = db.Column(db.Boolean, default = False)
    is_library_created = db.Column(db.Boolean, default = False)
    user_music_platform = db.relationship('UserMusicPlatform')
    user_playlists = db.relationship('UserPlaylists')
    user_tracks = db.relationship('UserTracks')
    user_artists_genres = db.relationship('UserArtists')


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
    refresh_token = db.Column(db.String(131))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, music_platform_name, music_platform_id, access_token, refresh_token, user_id):
        self.music_platform_name = music_platform_name
        self.music_platform_id = music_platform_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id

    def __repr__(self):
        return f"<User of {self.music_platform_name}, music_platform_id: {self.music_platform_id}>"


class UserPlaylists(db.Model):
    __tablename__ = "users_playlists"

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.String(25), unique=True)
    playlist_name = db.Column(db.String(100))
    is_owner = db.Column(db.Boolean)
    display_in_library = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, playlist_id, playlist_name, is_owner, display_in_library, user_id):
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.is_owner = is_owner
        self.display_in_library = display_in_library
        self.user_id = user_id

    def __repr__(self):
        return f"<Playlist: {self.playlist_name}>"


class UserTracks(db.Model):
    __tablename__ = "users_tracks"

    id = db.Column(db.Integer, primary_key=True)
    track_uri = db.Column(db.String(36))
    playlist_id_or_saved_song = db.Column(db.String(25))
    display_in_library = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, track_uri, playlist_id_or_saved_song, display_in_library, user_id):
        self.track_uri = track_uri
        self.playlist_id_or_saved_song = playlist_id_or_saved_song
        self.display_in_library = display_in_library
        self.user_id = user_id

    def __repr__(self):
        return f"<Track_uri: {self.track_uri}, owner_id: {self.user_id}>" 


class UserArtists(db.Model):
    __tablename__ = "users_artists"

    id = db.Column(db.Integer, primary_key=True)
    artist_uri = db.Column(db.String(37), unique=True)
    artist_name = db.Column(db.String(50))
    artist_main_genre_custom = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    artist_subgenre_custom = db.Column(db.String(30))
    __table_args__ = (UniqueConstraint('artist_uri', 'user_id'),)

    def __init__(self, artist_uri, artist_name, artist_main_genre_custom, artist_subgenre_custom, user_id):
        self.artist_uri = artist_uri
        self.artist_name = artist_name
        self.artist_main_genre_custom = artist_main_genre_custom
        self.artist_subgenre_custom = artist_subgenre_custom
        self.user_id = user_id

    def __repr__(self):
        return f"<Artist_name: {self.artist_name}, genre: {self.artist_main_genre_custom}, owner_id: {self.user_id}>"


class Artists(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    artist_uri = db.Column(db.String(37), unique=True)
    artist_name = db.Column(db.String(50))
    artist_genres = db.Column(db.String(300))
    artist_main_genre = db.Column(db.String(20))
    artist_subgenre = db.Column(db.String(30))

    def __init__(self, artist_uri, artist_name, artist_genres, artist_main_genre, artist_subgenre):
        self.artist_uri = artist_uri
        self.artist_name = artist_name
        self.artist_genres = artist_genres
        self.artist_main_genre = artist_main_genre
        self.artist_subgenre = artist_subgenre

    def __repr__(self):
        return f"<Artist_name: {self.artist_name}, genre: {self.artist_main_genre}, subgenre: {self.artist_subgenre}>"


class Tracks(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    track_uri = db.Column(db.String(36), unique=True)
    track_artist_main = db.Column(db.String(100))
    main_artist_uri = db.Column(db.String(37))
    track_artist_add1 = db.Column(db.String(100))
    track_artist_add2 = db.Column(db.String(100))
    track_title = db.Column(db.String(100))
    album_artist_main = db.Column(db.String(100))
    album_artist_add1 = db.Column(db.String(100))
    album_artist_add2 = db.Column(db.String(100))
    album_title = db.Column(db.String(100))
    album_uri = db.Column(db.String(36))

    def __init__(self, track_uri, track_artist_main, main_artist_uri, track_artist_add1, track_artist_add2,
                 track_title, album_artist_main, album_artist_add1, album_artist_add2, album_title, album_uri):
        self.track_uri = track_uri
        self.track_artist_main = track_artist_main
        self.main_artist_uri = main_artist_uri
        self.track_artist_add1 = track_artist_add1
        self.track_artist_add2 = track_artist_add2
        self.track_title = track_title
        self.album_artist_main = album_artist_main
        self.album_artist_add1 = album_artist_add1
        self.album_artist_add2 = album_artist_add2
        self.album_title = album_title
        self.album_uri = album_uri

    def __repr__(self):
        return f"<Track_title: {self.track_title}, track_artist: {self.track_artist_main}"


class Genre(db.Model):
    __tablename__ = "genres_subgenres"

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(30))
    subgenre = db.Column(db.String(30))

    def __init__(self, genre, subgenre):
        self.genre = genre
        self.subgenre = subgenre


class UserSettings(db.Model):
    __tablename__ = "users_settings"

    id = db.Column(db.Integer, primary_key=True)
    no_of_songs_into_folder = db.Column(db.Integer, default=3)
    include_songs_from_playlists = db.Column(db.Boolean, default=True)
    include_followed_playlists = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    def __init__(self, user_id):
        self.user_id = user_id