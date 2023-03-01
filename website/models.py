from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Grouping_Match():
    role = db.Column(db.String(15)) # Student, Organizer, Advisor
    grouping = db.Column(db.Integer(), db.ForeignKey("grouping.id"))


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key lowercase, 1 to many relationship (1 user many notes)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    # notes = db.relationship('Note') #relationship capital
    groupings = db.relationship("Grouping_Match")
    active_groupings = db.relationship("Grouping")

class Grouping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    student_roster = db.relationship("User")
    group_list = db.relationship("Group")
    creation_step = db.Column(db.Integer)
    student_form_responses = db.relationship("Student_Form")
    project_settings = db.relationship("Project_Settings")

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    spots = db.Column(db.Integer)
    cur_students = db.relationship("User")
    locked_students = db.relationship("User")
    banned_students = db.relationship("User")
    active = db.Column(db.Boolean)

class Student_Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranks = db.Column()

class project_Settings(db.Model):
    pass
