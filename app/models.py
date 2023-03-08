from app import db
from flask_login import UserMixin


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # foreign key for activity table
    calendarEvents = db.relationship('Calendar', backref='activity')

    # link to user bookings table
    #bookings = db.relationship('UserBookings', backref='calendar_user')

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activityType = db.Column(db.String(250), unique=True)

    activityDate = db.Column(db.Date, nullable=False)
    activityTime = db.Column(db.Integer, nullable=False)
    activityDuration = db.Column(db.Integer, nullable=False)    
    activityStaffName = db.Column(db.String(250))
    activityPrice = db.Column(db.Float)
    activityCapacity = db.Column(db.Integer)

    #this is the number of people signed up to the activity, which will need to be incremented
    activitySlotsTaken = db.Column(db.Integer)

    # Relationship with calendar
    activityId = db.Column(db.Integer, db.ForeignKey('activity.id'))


class UserBookings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # can be added once we have the userLogin table

    userId = db.Column(db.Integer)
    calendarId = db.Column(db.Integer)
    # userId = db.Column(db.Integer, db.ForeignKey('UserLogin.id'))
    # calendarId = db.Column(db.Integer, db.ForeignKey('calendar.id'))


# table to store payment cards
class PaymentCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardName = db.Column(db.String(100))
    cardNum = db.Column(db.Integer)
    cardCVV = db.Column(db.Integer)
    cardExpDate = db.Column(db.Date)

    # when there is a user table, user id will be made to be a foreign key.
    

# Login details
class UserLogin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # userId
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)  # Encrypt (Hash)
    #Customer is userType 1, Employee is userType 2, and Manager is useType3
    userType = db.Column(db.Integer, nullable=False) 

    userDetails = db.relationship('UserDetails', backref='loginDetails', uselist=False)


# User info (Sensitive info -> encryption)
class UserDetails(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # userDetailId
    name = db.Column(db.String(150), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(150))

    parentId = db.Column(db.Integer, db.ForeignKey('user_login.id'))
