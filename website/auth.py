from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User 
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)  # Creating a blueprint instance


# Blueprints and endpoints of the application
@auth.route('/login', methods=['GET', 'POST'])
def login():  # The login route
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in sucessfully!', category='success')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exists.', category='error')

    return render_template("login.html")


@auth.route('/logout')
def logout():  # Logging out function
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():  # Registering applications
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        # Inputs validation
        if user:  # Check for duplicate emails
            flash('Email already exists.', category='error')
        elif len(email) < 4:  # Email validation
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstname) < 2:  # First name limit
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:  # Password confirm
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:  # Password limit
            flash('Password must be at least 7 characters.', category='error')
        else:  # Creating a new user
            newUser = User(email=email, first_name=firstname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(newUser)  # Commit the new user to database
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))  # Redirecting to home page


    return render_template("sign_up.html")
