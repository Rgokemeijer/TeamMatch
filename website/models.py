from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Project_Match():
    role = db.Column(db.String(15)) # Student, Organizer, Advisor
    project = db.Column(db.Integer(), db.ForeignKey("project.id"))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key lowercase, 1 to many relationship (1 user many notes)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    notes = db.relationship('Note') #relationship capital
    projects = db.relationship("Project")

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    student_roster = db.relationship("Student_Roster")

class Student_Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150))

