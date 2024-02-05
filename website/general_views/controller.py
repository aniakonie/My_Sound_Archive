from website.database.models import db, User
from flask import request
from flask_login import login_user, current_user, logout_user

def sign_up(form):
    if request.method == 'POST':
        #add a case in which user with given username already exists
        new_user = User(form.username.data, form.password.data)
        new_user.authenticated = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return True

def log_in(form):
    if request.method == 'POST':
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return True
        else:
            return False
        
def log_out():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()