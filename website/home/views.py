from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, session
from website.database.models import *
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import generate_password_hash, check_password_hash


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
    username = current_user.username

    if request.method == "POST":




        if request.form["delete_account"] == "Delete my account":
            return redirect(url_for("home_bp.delete_account"))



    return render_template("home/settings.html", username = username, current = 'settings')


@home_bp.route('/delete_account', methods=["GET", "POST"])
@login_required
def delete_account():
    user_id = current_user.id
    if request.method == "POST":
        if request.form["answer"] == "Yes":
            if current_user.is_library_created == True:
                delete_library(user_id)
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

    user_music_platform = UserMusicPlatform.query.filter_by(user_id=user_id).first()
    db.session.delete(user_music_platform)
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


def delete_vml_account(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()    
    print("VML account deleted")


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)