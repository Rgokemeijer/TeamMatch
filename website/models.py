from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key lowercase, 1 to many relationship (1 user many notes)

class Grouping_Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15)) # Student, Organizer, Advisor
    grouping = db.Column(db.Integer(), db.ForeignKey("grouping.id"))
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    # notes = db.relationship('Note') #relationship capital
    groupings = db.relationship('Grouping_Relationship') #relationship capital
    active_grouping = db.Column(db.Integer(), db.ForeignKey("grouping.id"))

class Grouping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    student_roster = db.relationship("User")
    group_list = db.relationship("Group")
    creation_step = db.Column(db.Integer)
    student_form_responses = db.relationship("Student_Form")
    grouping_settings = db.relationship("Grouping_Settings")

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    grouping = db.Column(db.Integer, db.ForeignKey("grouping.id"))
    spots = db.Column(db.Integer)
    # cur_students = db.relationship("User") Do not know how to implement
    # locked_students = db.relationship("User")
    # banned_students = db.relationship("User")
    active = db.Column(db.Boolean)

class Student_Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grouping = db.Column(db.Integer, db.ForeignKey("grouping.id"))
    # ranks = db.Relationship("Group") Also do not know how to work

class Grouping_Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grouping = db.Column(db.Integer, db.ForeignKey("grouping.id"))
