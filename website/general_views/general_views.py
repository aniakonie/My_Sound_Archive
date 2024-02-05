from flask import render_template, redirect, url_for, request
from flask import Blueprint
from website.database.models import login_manager, User
from flask_login import login_required, current_user
from website.general_views.controller import *

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=30)])


general_views_bp = Blueprint('general_views_bp', __name__, template_folder='templates')

@general_views_bp.route('/')
def home():
    return render_template("general_views/home.html")

@general_views_bp.route('/how_it_works')
def how_it_works():
    return render_template("general_views/how_it_works.html", current = "how_it_works")

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@general_views_bp.route('/sign-up', methods=["GET", "POST"])
def sign_up_view():

    form = LoginForm()
    new_user_added = sign_up(form)
    if new_user_added:
        return redirect(url_for("general_views_bp.log_in_to_spotify_view"))

    return render_template("general_views/sign-up.html", form = form)


@general_views_bp.route('/login', methods=["GET", "POST"])
def login_view():
    form = LoginForm()
    user_logged_in = log_in(form)
    if user_logged_in:
        return redirect(url_for("general_views_bp.account_page_view"))

    return render_template("general_views/login.html", form = form)


@general_views_bp.route('/logout')
@login_required
def log_out_view():
    log_out()
    return redirect(url_for("general_views_bp.home"))


@general_views_bp.route('/log_in_to_spotify')
@login_required
def log_in_to_spotify_view():
    return render_template("general_views/log_in_to_spotify.html")


@general_views_bp.route('/account_page')
@login_required
def account_page_view():
    username = current_user.username
    return render_template("general_views/account_page.html", username = username)