from flask import render_template, redirect, url_for, request
from flask import Blueprint
from website.database.models import login_manager, User, db
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


home_bp = Blueprint('home_bp', __name__, template_folder='templates')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=30)])


@home_bp.route('/')
def home():
    return render_template("home/home.html")


@home_bp.route('/how_it_works')
def how_it_works():
    return render_template("home/how_it_works.html", current = "how_it_works")


@home_bp.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    form = LoginForm()
    if request.method == 'POST':
        #add a case in which user with given username already exists
        new_user = User(form.username.data, form.password.data)
        new_user.authenticated = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for("home_bp.log_in_to_spotify"))
    return render_template("home/sign-up.html", form = form)


@home_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("home_bp.account"))
        else:
            pass #TODO flash_message_wrong_password

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


@home_bp.route('/log_in_to_spotify')
@login_required
def log_in_to_spotify():
    username = current_user.username
    return render_template("home/log_in_to_spotify.html", username = username)


@home_bp.route('/account')
@login_required
def account():
    username = current_user.username
    return render_template("home/account.html", username = username)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)