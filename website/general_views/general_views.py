from flask import render_template
from flask import Blueprint

general_views_bp = Blueprint('general_views_bp', __name__, template_folder='templates')

@general_views_bp.route('/')
def home():
    return render_template("general_views/home.html")

@general_views_bp.route('/how_it_works')
def how_it_works():
    return render_template("general_views/how_it_works.html", current = "how_it_works")

