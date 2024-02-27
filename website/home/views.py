from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, session
from website.database.models import login_manager, User, db
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


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
        if form.username.data in  all_usernames:
            flash('Such user already exists. Please choose different username.', category="error")
        else:
            new_user = User(form.username.data, form.password.data)
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
            if user.password == form.password.data:
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
        session["allowed"] = True
        return redirect(url_for("spotify_bp.authorization"))
    return render_template("home/log_in_to_spotify.html", username = username)


@home_bp.route('/settings')
@login_required
def settings():
    username = current_user.username
    return render_template("home/settings.html", username = username, current = 'settings')


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


