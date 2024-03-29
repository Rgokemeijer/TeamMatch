"""
File to handle the backend of all the webpages that can be accessed once logged in.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import StudentRoster, Project, Ranks, User
from . import db
import numpy as np
from .algorithm import algo
views = Blueprint('views', __name__)


#home page
@views.route('/', methods =["GET", "POST"])
@login_required
def home():
    rosters = StudentRoster.query.filter_by(email = current_user.email).all() #gets all the students associated with this account
    return render_template("home.html", rosters=rosters, user=current_user) #in template check if current_user is authenticated

#help page
@views.route('/help')
@login_required
def help():
    return render_template("help.html", user=current_user) #in template check if current_user is authenticated

#page to view/add/remove students from the roster i.e students you want to be assigned to groups
@views.route("/studentroster")
@login_required
def studentroster():
    contList=StudentRoster.query.filter_by(ownerID = current_user.id).all() #all students that have currently been added
    cont=StudentRoster.query.first()
    return render_template("student_roster.html", cont=cont, contList=contList, user = current_user)

#code to handle when a user adds a student from the studentroster page
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
    """
    code to handle when a user removes a student from the studentroster page
    mid: id of the student to be removed
    """
    student = StudentRoster.query.filter_by(contactID=mid).first() #queries the student to be deleted
    if student:
        for rank in student.ranks:
            db.session.delete(rank)
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for('views.studentroster'))

#page to view/add/remove projects that are to be associated with groupings
@views.route("/projects")
@login_required
def projects():
    contList=Project.query.filter_by(projectownerID = current_user.id).all() #get all the projects that have been added
    cont=Project.query.first()
    return render_template("projects.html", cont=cont, contList=contList, user = current_user)

#code to handle when a user adds a project
@views.route("/addproject", methods=["POST"])
@login_required
def addproject():
    #store values recieved from HTML form in local variables
    mentorfName=request.form.get("Mentor FirstName")
    mentorlName=request.form.get("Mentor LastName")
    projectName=request.form.get("Project Name")
    #Pass on the local values to the corresponfding model
    project = Project( projectName = projectName, mentorfName=mentorfName, mentorlName=mentorlName, projectownerID = current_user.id)
    db.session.add(project)
    db.session.commit()
    # query all projects that are owned by this user
    # cont=Project.query.filter_by(projectownerID=current_user.id).first()
    contList=Project.query.filter_by(projectownerID=current_user.id).all()
    return render_template("projects.html", contList=contList, user = current_user) 

@views.route("/deleteproject/<mid>", methods=["POST"]) 
@login_required
def deleteproject(mid):
    """
    code to handle when a user removes a project
    mid: id of project to be removed
    """
    project = Project.query.filter_by(projectID=mid).first()
    if project:
        ranks = Ranks.query.filter_by(projectID=project.projectID).all()
        for rank in ranks:
            db.session.delete(rank)
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for('views.projects'))

@views.route("/studentrankings/<mid>/<conID>", methods = ['GET', 'POST']) 
@login_required
def studentrankings(mid, conID):
    """
    Page to allow students to rank projects
    mid: id of the owner of the grouping (the one who assigned these projects to you to be ranked)
    conID: ID of the roster (the ID of the student these rankings will be associated with)
    """
   
    owner = User.query.filter_by(id=mid).first() #gets user information of the owner of this grouping
    projects = owner.project #get projects associated with this grouping
    if request.method == 'POST': #if the user is submitting rankings
        for i in range(1,1+len(projects)):
            proj_id = request.form.get(f'Rank{i}') # get which project ranked first
            #print(proj_id)
            if proj_id is None: #if the student didn't rank every project
                flash('Please rank all projects once', category = 'error')
                return render_template("rankings.html", projects = projects, num_projects=len(projects), user = current_user)
            #check if a ranking has already been submitted
            cur_ranking = Ranks.query.filter_by(rosterID=conID, rank=i).first()
            if cur_ranking is None:
                # if it has not create one
                stud_ranks_obj = Ranks(rosterID = conID, rank=i, projectID=proj_id)
                db.session.add(stud_ranks_obj)
            else: #else update the ranking
                cur_ranking.projectID = proj_id
        db.session.commit()
        flash('Submitted Rankings', category = 'success')
        return redirect(url_for('views.home'))
    return render_template("rankings.html", projects = projects, num_projects=len(projects), user = current_user)

#page for the user to create groups based on rankings
@views.route("/createGroups", methods = ['GET', 'POST']) 
@login_required
def createGroups():
    # Returns a roster of all students who are in this grouping
    rosters = StudentRoster.query.filter_by(ownerID=current_user.id).all() 
    if len(rosters) == 0:
        flash("Your roster is empty", category='error')
        return redirect(url_for('views.home'))
    # each student roster has the same list of projects that
    # get one of them
    owner = User.query.filter_by(id=current_user.id).first()
    projects = owner.project
    # this will populate with each students ranks of the projects
    ranks = np.full((len(rosters), len(projects)), (len(projects)+1)**2)
    #orders project ids to add to and search for later in ranks array
    proj_index_lookup = []
    groups = {} #dictionary, project name goes to list of students
    for project in projects:
        proj_index_lookup.append(project.projectID)
        # this is where students will be placed when locked into a group
        groups[project.projectName] = []
    proj_index_lookup.sort()
    #orders studentroster ids to search for later in ranks array
    student_index_lookup = []
    for student in rosters:
        # get teh students ID from the student roster row
        student_index_lookup.append(student.contactID)
    student_index_lookup.sort()
    #put all rankings into array
    for student in rosters:
        student_rankings = student.ranks
        for rank in student_rankings:
            ranks[student_index_lookup.index(student.contactID)][proj_index_lookup.index(rank.projectID)] = rank.rank**2  #if it needs to start at 0 then have -1 

    single_array_ranks = ranks.flatten() #turns 2d array to 1d
    result = algo(single_array_ranks, len(rosters), len(projects)) #run grouping algorith
    i = 0
    for student in result:
        group_num = np.where(student == 1)
        group_num = group_num[0][0] #get what group num they are in (indexed according to proj_index_lookup)
        proj = Project.query.filter_by(projectID = proj_index_lookup[group_num]).first() #find what project the student is assigned to
        proj_name = proj.projectName
        stud = StudentRoster.query.filter_by(contactID = student_index_lookup[i]).first() #find the name of the student
        stud_name = stud.fName + " " + stud.lName
        i += 1
        groups[proj_name].append(stud_name) #associate student with project in dictionary
    
    #show student rankings
    stud_ranks = {}
    for i, student in enumerate(rosters):
        stud_name = student.fName + " " + student.lName
        stud_ranks[stud_name] = []
        for project in projects:
            rank = Ranks.query.filter_by(projectID = project.projectID, rosterID=student.contactID).first()
            if rank is not None:
                stud_ranks[stud_name].append(rank.rank)
            else:
                stud_ranks[stud_name].append("N/A") 
    
    return render_template("createGroups.html", rankings = stud_ranks, projects=projects, groups = groups, user=current_user)


#currently someone can resubmit rankings and it just adds more 
#instead of overriding
#print(item.project)