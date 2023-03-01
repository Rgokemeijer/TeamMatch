from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Grouping, Grouping_Relationship, User
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
            grouping = Grouping(name="Untitled Grouping")
            grouping_relation = Grouping_Relationship(role="O", grouping=grouping.id)
            db.session.add(grouping, grouping_relation) 
            db.session.commit() # must be before active_grouping call to set id to not None
            current_user.groupings.append(grouping_relation)
            current_user.active_grouping = grouping.id
            db.session.commit()

            return redirect(url_for('views.roster_create'))
        else:
            return redirect(url_for('views.roster_create'))
    return render_template("home.html", user=current_user, projects=current_user.groupings) #in template check if current_user is authenticated

@views.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template("roster_create.html", user=current_user, project_names=current_user.projects.project_name)

@views.route('/create_grouping/upload_roster', methods=['GET', 'POST'])
@login_required
def roster_create():
    print("active:", current_user.active_grouping, file=sys.stderr)
    active_grouping = Grouping.query.filter_by(id=current_user.active_grouping).one()
    if request.method == 'POST' and request.form.get("submit") != None:
        if request.form.get("submit")[0] == "D":
            email = request.form.get("submit")[1:]
            active_grouping.query.filter_by(email=email).delete()
        print(request.form.get("submit"), file=sys.stderr)
    students = active_grouping.student_roster
    return render_template("roster_create.html", user=current_user, students=students)
