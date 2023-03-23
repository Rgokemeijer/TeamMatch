from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import StudentRoster
from . import db
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user) #in template check if current_user is authenticated

@views.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template("roster_create.html", user=current_user)


@views.route("/studentroster")
@login_required
def studentroster():
    contList=StudentRoster.query.filter_by(ownerID = current_user.id).all()
    cont=StudentRoster.query.first()
    return render_template("student_roster.html", cont=cont, contList=contList, user = current_user)
    
@views.route("/addstudent", methods=["POST"])
@login_required
def addstudent():
    #store values recieved from HTML form in local variables
    fName=request.form.get("FirstName")
    lName=request.form.get("LastName")
    email=request.form.get("email")
    #Pass on the local values to the corresponfding model
    student = StudentRoster( fName=fName, lName=lName,email=email, ownerID = current_user.id)
    db.session.add(student)
    db.session.commit()
    cont=StudentRoster.query.filter_by(email=email).first()
    contList=StudentRoster.query.all()
    return render_template("student_roster.html",cont=cont, contList=contList, user = current_user) 

@views.route("/deletestudent/<mid>", methods=["POST"]) 
@login_required
def deletestudent(mid):
    merch = StudentRoster.query.filter_by(email=mid).first()
    if merch:
        db.session.delete(merch)
        db.session.commit()
    return redirect(url_for('views.studentroster'))