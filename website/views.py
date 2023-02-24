from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Student_Roster, Project
from . import db
# for print delete for production
import sys

views = Blueprint('views', __name__)


@views.route('/', methods =["GET", "POST"])
@login_required
def home():
    if request.method == 'POST' and request.form.get("submit") != None:
        print(request.form.get("submit"), file=sys.stderr)
        print(type(request.form.get("submit")), file=sys.stderr)
        if request.form.get("submit") == "CG":
            print("yup",request.form.get("submit"), file=sys.stderr)
            project = Project(name="Untitled Grouping")
            current_user.projects.append(project)
            # db.session.add(project) 
            # db.session.commit()
            return redirect(url_for('views.roster_create'))
        else:
            return render_template("home.html", user=current_user)

            # return redirect(url_for('views.roster_create'))
    
    return render_template("home.html", user=current_user, projects=current_user.projects) #in template check if current_user is authenticated

@views.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template("roster_create.html", user=current_user, project_names=current_user.projects.project_name)

@views.route('/create_grouping/upload_roster', methods=['GET', 'POST'])
@login_required
def roster_create():
    if request.method == 'POST' and request.form.get("submit") != None:
        if request.form.get("submit")[0] == "D":
            email = request.form.get("submit")[1:]
            Student_Roster.query.filter_by(email=email).delete()
        # print(request.form.get("submit"), file=sys.stderr)
    roster = Student_Roster(email="test", first_name="fname", last_name="lastname")
    db.session.add(roster) 
    db.session.commit() # adds to DB
    students = Student_Roster.query.all()
    return render_template("roster_create.html", user=current_user, students=students)
