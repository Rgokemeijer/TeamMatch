from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import StudentRoster, Project
from . import db
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    rosters = StudentRoster.query.filter_by(email = current_user.email).all()
    return render_template("home.html", rosters=rosters, user=current_user) #in template check if current_user is authenticated

@views.route('/help')
@login_required
def h3lp():
    return render_template("help.html", user=current_user) #in template check if current_user is authenticated

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
    contList=StudentRoster.query.filter_by(ownerID=current_user.id).all()
    return render_template("student_roster.html",cont=cont, contList=contList, user = current_user) 

@views.route("/deletestudent/<mid>", methods=["POST"]) 
@login_required
def deletestudent(mid):
    merch = StudentRoster.query.filter_by(contactID=mid).first()
    if merch:
        db.session.delete(merch)
        db.session.commit()
    return redirect(url_for('views.studentroster'))


@views.route("/projects")
@login_required
def projects():
    contList=Project.query.filter_by(projectownerID = current_user.id).all()
    cont=Project.query.first()
    return render_template("projects.html", cont=cont, contList=contList, user = current_user)
    
@views.route("/addproject", methods=["POST"])
@login_required
def addproject():
    #store values recieved from HTML form in local variables
    mentorfName=request.form.get("Mentor FirstName")
    mentorlName=request.form.get("Mentor LastName")
    projectName=request.form.get("Project Name")
    #Pass on the local values to the corresponfding model
    project = Project( projectName = projectName, mentorfName=mentorfName, mentorlName=mentorlName, projectownerID = current_user.id, rosterprojectconnect = current_user.id)
    db.session.add(project)
    db.session.commit()
    cont=Project.query.filter_by(projectownerID=current_user.id).first()
    contList=Project.query.filter_by(projectownerID=current_user.id).all()
    return render_template("projects.html",cont=cont, contList=contList, user = current_user) 

@views.route("/deleteproject/<mid>", methods=["POST"]) 
@login_required
def deleteproject(mid):
    merch = Project.query.filter_by(projectID=mid).first()
    if merch:
        db.session.delete(merch)
        db.session.commit()
    return redirect(url_for('views.projects'))

@views.route("/studentrankings/<mid>", methods = ['GET', 'POST']) 
@login_required
def studentrankings(mid):
    if request.method == 'POST':
        rank1 = request.form.get('Rank1')
        rank2 = request.form.get('Rank2')
        rank3 = request.form.get('Rank3')
        rank4 = request.form.get('Rank4')
        rank5 = request.form.get('Rank5')
        print(rank1, rank2, rank3, rank4, rank5)
   
   
    rosters = StudentRoster.query.filter_by(ownerID=mid).first()
  
    projects = rosters.project
    proj = []
    for item in projects:
       proj.append(item.projectName)
    projects = []
    
    return render_template("rankings.html", projects = proj, user = current_user)

#now i need to get rankings into database to be used