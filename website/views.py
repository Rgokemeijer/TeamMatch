from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user) #in template check if current_user is authenticated

@views.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template("roster_create.html", user=current_user)
