from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

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