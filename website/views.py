from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Student_Roster
from . import db

views = Blueprint('views', __name__)

<<<<<<< HEAD
@views.route('/', methods =["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        return redirect(url_for('views.groupings', user = current_user))
    elif request.method == 'GET':
        return render_template("home.html", user=current_user) #in template check if current_user is authenticated

@views.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template("roster_create.html", user=current_user)

@views.route('/groupings', methods=['GET',"POST"])
@login_required
def groupings():
    return render_template("roster_create.html", user=current_user)
=======
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        return redirect(url_for('views.roster_create'))
    return render_template("home.html", user=current_user) #in template check if current_user is authenticated

@views.route('/create_grouping/upload_roster', methods=['GET', 'POST'])
def roster_create():
    roster = Student_Roster(email="test", first_name="fname", last_name="lastname")
    db.session.add(roster) 
    db.session.commit() # adds to DB
    students = Student_Roster.query.all()
    return render_template("roster_create.html", user=current_user, students=students)
>>>>>>> 5f4f602b4c10e2c05c4bd47a185ba29e9349ec9f
