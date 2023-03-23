from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#class Note(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  data = db.Column(db.String(10000))
   # date = db.Column(db.DateTime(timezone=True), default=func.now())
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key lowercase, 1 to many relationship (1 user many notes)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    #notes = db.relationship('Note') #relationship capital
    student_roster = db.relationship('StudentRoster')

class StudentRoster(db.Model):
    __tablename__="studentroster"
    contactID = db.Column(db.Integer, primary_key=True)
    fName =db.Column(db.String, nullable=False)
    lName =db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    ownerID = db.Column(db.Integer, db.ForeignKey('user.id'))

