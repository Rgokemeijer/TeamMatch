"""
File to handle backend of creating user accounts and logging in
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth  = Blueprint('auth', __name__)

#function to serve the login page and login
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST': #hit submit to try and login
        #gets login info from text fields
        email =request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #look in db by column to find if user exists
        if user:
            if check_password_hash(user.password, password): #ensure the password is correct
                flash('Logged in successfully', category = 'success')
                login_user(user, remember=True) #remembers user is logged in in session
                return redirect(url_for('views.home')) #go to home page
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email doesn\'t exist', category='error')
    return render_template("login.html", user=current_user)

#function to log the user out and return to login page
@auth.route('/logout')
@login_required #cant access page if not logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#function to handle creating user accounts
@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST': #if user hit submit to create an account
        #get info from input fields
        email = request.form.get('email')
        email2 = request.form.get('email2')
        firstName = request.form.get('firstName')
        lastName  = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user: #make sure user doesn't exist
            flash('Email already exists', category = 'error')
        
        #the following is checks on inputted info
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('firstname must be greater than 2 characters.', category='error')
        elif len(lastName) < 2:
            flash('lastname must be greater than 2 characters.', category='error')
        elif password1 != password2:
           flash('Passwords do not match.', category = 'error')
        elif email != email2:
            flash('Email addresses do not match.', category='error')
        else: #can successfully create account
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user) 
            db.session.commit() #adds to db
            login_user(new_user, remember=True) #logs the user in
            flash('Account created!', category = 'success')
            return redirect(url_for('views.home')) #takes you to the home page
    return render_template("sign_up.html", user=current_user)