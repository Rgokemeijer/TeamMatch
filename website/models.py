"""
File to hold all the database schemas
"""
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#class Note(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  data = db.Column(db.String(10000))
   # date = db.Column(db.DateTime(timezone=True), default=func.now())
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key lowercase, 1 to many relationship (1 user many notes)

#schema for user accounts
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    #notes = db.relationship('Note') #relationship capital
    student_roster = db.relationship('StudentRoster') #one to many relationship to rosters; added to when user updates roster on site
    project = db.relationship('Project') #one to many relationship to projects; added to when user adds projects on site

#schema for all the students a user has added to their roster
class StudentRoster(db.Model):
    __tablename__="studentroster"
    contactID = db.Column(db.Integer, primary_key=True)
    #student info
    fName =db.Column(db.String, nullable=False)
    lName =db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    #the id and emmail of the user who owns/created this roster
    ownerID = db.Column(db.Integer, db.ForeignKey('user.id'))
    ownerEmail = db.Column(db.String, nullable=False)

    ranks = db.relationship('Ranks') # one to many relationship with ranks; holds the project rankings of specific students

#schema for all projects a user has added
class Project(db.Model):
    __tablename__="project"
    projectID = db.Column(db.Integer, primary_key=True)
    projectName =db.Column(db.String, nullable=False)
    mentorfName =db.Column(db.String, nullable=False)
    mentorlName =db.Column(db.String, nullable=False)
    projectownerID = db.Column(db.Integer, db.ForeignKey('user.id')) #the id of the user who added this project

#schema to hold students' rankings for projects
class Ranks(db.Model):
    rankID = db.Column(db.Integer, primary_key=True)
    rosterID = db.Column(db.Integer, db.ForeignKey('studentroster.contactID')) #students associated with this ranking
    rank = db.Column(db.Integer) #rank given to this project
    projectID = db.Column(db.Integer) #id of project ranked



#link studentroster to project 1 to many relationship
#in project foreignkey make ownerc current_user like previously
#then when student logs in query rosters by their email
#with all those queries you then can loop through and look at linked projects
#by querying the 1 to many element


#student logs in
#queries all rosters filtered by their email
#from that query get ownerid of roster
#with ownerid query projects
