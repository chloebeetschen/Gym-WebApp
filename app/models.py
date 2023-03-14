from app import db
from flask_login import UserMixin


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    activityType = db.Column(db.String(250), unique=True)

    # foreign key for activity table
    calendarEvents = db.relationship('Calendar', backref='activity')

    # link to user bookings table
    #bookings = db.relationship('UserBookings', backref='calendar_user')


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    aDateTime  = db.Column(db.DateTime, nullable=False)
    aDuration  = db.Column(db.Integer, nullable=False)    
    aStaffName = db.Column(db.String(250))
    aLocation  = db.Column(db.String(250))
    aPrice     = db.Column(db.Float)
    aCapacity  = db.Column(db.Integer)

    #this is the number of people signed up to the activity, which will need to be incremented
    aSlotsTaken = db.Column(db.Integer)

    # Relationship with calendar
    activityId = db.Column(db.Integer, db.ForeignKey('activity.id'))

    #relationship with user bookings
    userEvents = db.relationship('UserBookings', backref='calendar')


class UserBookings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # can be added once we have the userLogin table

    #userId = db.Column(db.Integer)
    #calendarId = db.Column(db.Integer)

    userId = db.Column(db.Integer, db.ForeignKey('user_login.id'))
    calendarId = db.Column(db.Integer, db.ForeignKey('calendar.id'))


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

    #relationship with userbookings
    userbookings = db.relationship('UserBookings', backref='loginDetails')


# User info (Sensitive info -> encryption)
class UserDetails(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # userDetailId
    name = db.Column(db.String(150), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(150))
    isMember = db.Column(db.Boolean)
    membershipEnd = db.Column(db.DateTime)
    parentId = db.Column(db.Integer, db.ForeignKey('user_login.id'))
