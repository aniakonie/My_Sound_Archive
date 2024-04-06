from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, session, request
from website.database.models import *
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import and_
from website.library.views import get_genres, get_subgenres

home_bp = Blueprint('home_bp', __name__, template_folder='templates')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=30)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


@home_bp.route('/')
def home():
    return render_template("home/home.html")

@home_bp.route('/how_it_works')
def how_it_works():
    return render_template("home/how_it_works.html")


@home_bp.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("library_bp.library"))
    
    form = SignUpForm()
    if request.method == 'POST':
        all_usernames = User.query.all()
        all_usernames = [user.username for user in all_usernames]
        if form.username.data in all_usernames:
            flash('Such user already exists. Please choose different username.', category="error")
        else:
            hashed_password = generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(form.username.data, hashed_password)
            new_user.authenticated = True
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for("home_bp.log_in_to_spotify"))
    return render_template("home/sign-up.html", form = form)


@home_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("library_bp.library"))

    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            is_valid = check_password_hash(user.password, form.password.data)
            if is_valid:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("library_bp.library"))
            else:
                flash('Wrong login credentials', category = "error")
                return redirect(url_for("home_bp.login")) 
        else:
            flash('Wrong login credentials', category = "error")
            return redirect(url_for("home_bp.login")) 
    return render_template("home/login.html", form = form)


@home_bp.route('/logout')
@login_required
def log_out():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("home_bp.home"))


@home_bp.route('/log_in_to_spotify', methods=["GET", "POST"])
@login_required
def log_in_to_spotify():
    if current_user.is_library_created:
        abort(401)
    username = current_user.username
    if request.method == 'POST':
        return redirect(url_for("spotify_bp.authorization"))
    return render_template("home/log_in_to_spotify.html", username = username)


@home_bp.route('/settings', methods=["GET", "POST"])
@login_required
def settings():

    if current_user.is_library_created:
        user_playlists_included, user_playlists_excluded = get_user_playlists()
        user_id = current_user.id
        genres = get_genres(user_id)
        genres_subgenres = []
        for genre in genres:
            subgenres = get_subgenres(genre, user_id)
            genres_subgenres.append({"genre":genre, "subgenres": subgenres})
    else: user_playlists_included = user_playlists_excluded = genres_subgenres = None


    if request.method == "POST":
        number_of_songs_into_folders = request.form.get("number_of_songs_into_folders")
        playlist_id_exclude = request.form.get("selected_playlist_id_exclude")
        playlist_id_include = request.form.get("selected_playlist_id_include")
        genre_subgenre_browse = request.form.get("genre_subgenre_browse")

        if number_of_songs_into_folders:
            change_number_of_songs_into_folders(number_of_songs_into_folders)
            flash('Changes have been saved', category = "success")
            return redirect(url_for("home_bp.settings"))

        elif playlist_id_exclude or playlist_id_include:
            change_display_to = change_playlist_display_setting(playlist_id_exclude, playlist_id_include)
            if change_display_to == False:
                flash('Playlist has been excluded from your library', category = "success")
            else:
                flash('Playlist has been included in your library', category = "success")
            return redirect(url_for("home_bp.settings"))

        elif genre_subgenre_browse:
            print(genre_subgenre_browse)


            return redirect(url_for("home_bp.settings"))




        elif request.form.get("delete_account") == "Delete my account":
            return redirect(url_for("home_bp.delete_account"))
        
    return render_template("home/settings.html", current = 'settings', user_playlists_included=user_playlists_included, user_playlists_excluded=user_playlists_excluded,
                           genres_subgenres=genres_subgenres)


@home_bp.route('/delete_account', methods=["GET", "POST"])
@login_required
def delete_account():
    user_id = current_user.id
    if request.method == "POST":
        if request.form["answer"] == "Yes":
            if current_user.is_library_created == True:
                delete_library(user_id)
                delete_user_music_platform(user_id)
                delete_vml_account(user_id)
            else:
                delete_vml_account(user_id)
            flash('Your account has been deleted', category = "success")
            return redirect(url_for("home_bp.home"))
        else:
            return redirect(url_for("library_bp.library"))
    return render_template("home/delete_account.html", current = "delete_account")


def delete_library(user_id):
    user_settings = UserSettings.query.filter_by(user_id=user_id).first()
    db.session.delete(user_settings)
    db.session.commit()  

    models_to_delete = [UserTracks, UserPlaylists, UserArtists]
    for model in models_to_delete:
        user_records = model.query.filter_by(user_id=user_id).all()
        for record in user_records:
            db.session.delete(record)
    db.session.commit()

    user = User.query.filter_by(id=user_id).first()
    user.is_library_created = False
    db.session.add(user)
    db.session.commit()
    print("Library deleted")


def delete_user_music_platform(user_id):
    user_music_platform = UserMusicPlatform.query.filter_by(user_id=user_id).first()
    db.session.delete(user_music_platform)
    db.session.commit()


def delete_vml_account(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()    
    print("VML account deleted")


def get_user_playlists():
    user_playlists = UserPlaylists.query.filter_by(user_id = current_user.id).order_by('playlist_name').all()
    if not user_playlists:
        user_playlists_included = "no playlists"
        user_playlists_excluded = "no playlists"
    else:
        user_playlists_included = []
        user_playlists_excluded = []
        for playlist in user_playlists:
            if playlist.display_in_library == True:
                user_playlists_included.append((playlist.playlist_name, playlist.playlist_id))
            else:
                user_playlists_excluded.append((playlist.playlist_name, playlist.playlist_id))
    return user_playlists_included, user_playlists_excluded


def change_number_of_songs_into_folders(number_of_songs_into_folders):
    user = UserSettings.query.filter_by(user_id = current_user.id).first()
    user.no_of_songs_into_folder = number_of_songs_into_folders
    db.session.add(user)
    db.session.commit()


def change_playlist_display_setting(playlist_id_exclude, playlist_id_include):
    playlist_id_to_change = playlist_id_exclude if playlist_id_exclude is not None else playlist_id_include
    change_display_to = False if playlist_id_exclude is not None else True
    playlist_to_change = UserPlaylists.query.filter(and_(UserPlaylists.user_id == current_user.id, UserPlaylists.playlist_id == playlist_id_to_change)).first()
    playlist_to_change.display_in_library = change_display_to
    db.session.add(playlist_to_change)
    db.session.commit()
    user_tracks = UserTracks.query.filter(and_(UserTracks.user_id == current_user.id, UserTracks.playlist_id_or_saved_song == playlist_id_to_change)).all()
    for track in user_tracks:
        track.display_in_library = change_display_to
        db.session.add(track)
    db.session.commit()
    return change_display_to


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)