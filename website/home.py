from flask import Flask, render_template
from flask import Blueprint

home = Blueprint('home', '__name__')

@home.route('/')
def welcome():
    return render_template("home.html")

