from flask import Flask, render_template
from flask import Blueprint

home = Blueprint('home', '__name__')

@home.route('/')
def welcome():
    return render_template("home.html")

@home.route('/how_it_works')
def how_it_works():
    return render_template("how_it_works.html", current = "how_it_works")

