from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import StudentRoster, Project, Ranks
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
    student = StudentRoster( fName=fName, lName=lName,email=email, ownerID = current_user.id, ownerEmail = current_user.email)
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
def projects():#
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

@views.route("/studentrankings/<mid>/<conID>", methods = ['GET', 'POST']) 
@login_required
def studentrankings(mid, conID):
    if request.method == 'POST':
        rank1 = request.form.get('Rank1')
        rank2 = request.form.get('Rank2')
        rank3 = request.form.get('Rank3')
        rank4 = request.form.get('Rank4')
        rank5 = request.form.get('Rank5')    
        #print(rank1, rank2, rank3, rank4, rank5)
        rankOne = Ranks(rosterID = conID, rank=1, projectID=rank1)
        db.session.add(rankOne)
        db.session.commit()
        rankTwo = Ranks(rosterID = conID, rank=2, projectID=rank2)
        db.session.add(rankTwo)
        db.session.commit()
        rankThree = Ranks(rosterID = conID, rank=3, projectID=rank3)
        db.session.add(rankThree)
        db.session.commit()
        rankFour = Ranks(rosterID = conID, rank=4, projectID=rank4)
        db.session.add(rankFour)
        db.session.commit()
        rankFive = Ranks(rosterID = conID, rank=5, projectID=rank5)
        db.session.add(rankFive)
        db.session.commit()
        flash('Submitted Rankings', category = 'success')
        return redirect(url_for('views.home'))
    rosters = StudentRoster.query.filter_by(ownerID=mid).first() 
    projects = rosters.project
    proj = []
    for item in projects:
       proj.append(item)
    projects = []
    return render_template("rankings.html", projects = proj, user = current_user)

@views.route("/createGroups", methods = ['GET', 'POST']) 
@login_required
def createGroups():
    rosters = StudentRoster.query.filter_by(ownerID=current_user.id).all()
    stud_proj_rank = []
    for roster in rosters:
        ranks = roster.ranks
        for item in ranks:
            project = Project.query.filter_by(projectID = item.projectID).first()
            projName = project.projectName
            stud_proj_rank.append([roster.email, projName, item.rank])
    return render_template("createGroups.html", rankings = stud_proj_rank, user=current_user)


#currently someone can resubmit rankings and it just adds more 
#instead of overriding
