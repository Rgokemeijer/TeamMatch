from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Contacts
from . import db
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user) #in template check if current_user is authenticated

@views.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template("roster_create.html", user=current_user)


@views.route("/contacts")
@login_required
def index():
    contList=Contacts.query.filter_by(ownerID = current_user.id).all()
    cont=Contacts.query.first()
    return render_template("index.html", cont=cont, contList=contList, user = current_user)
    
@views.route("/addcontact", methods=["POST"])
@login_required
def addcontact():
    #store values recieved from HTML form in local variables
    fName=request.form.get("FirstName")
    lName=request.form.get("LastName")
    email=request.form.get("email")
    #Pass on the local values to the corresponfding model
    contact = Contacts( fName=fName, lName=lName,email=email, ownerID = current_user.id)
    db.session.add(contact)
    db.session.commit()
    cont=Contacts.query.filter_by(email=email).first()
    contList=Contacts.query.all()
    return render_template("index.html",cont=cont, contList=contList, user = current_user) 

@views.route("/contactdelete/<mid>", methods=["POST"]) 
@login_required
def contactdelete(mid):
    merch = Contacts.query.filter_by(email=mid).first()
    if merch:
        db.session.delete(merch)
        db.session.commit()
    return redirect(url_for('views.index'))