from app import db
from flask_login import UserMixin
from sqlalchemy.orm import validates, load_only
from datetime import *


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activityType = db.Column(db.String(250), nullable=False)
    # foreign key for activity table
    calendarEvents = db.relationship('Calendar', backref='activity')

    @staticmethod
    def create(activityType): 
        db.session.add(Activity(activityType))
        db.session.commit()


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aDateTime  = db.Column(db.DateTime, nullable=False)
    aDuration  = db.Column(db.Integer, nullable=False)    
    aStaffName = db.Column(db.String(250), nullable=False)
    aLocation  = db.Column(db.String(250), nullable=False)
    aPrice     = db.Column(db.Float, nullable=False)
    aCapacity  = db.Column(db.Integer, nullable=False)
    #this is the number of people signed up to the activity, which will need to be incremented
    aSlotsTaken = db.Column(db.Integer, nullable=False)
    #is it a daily repeated event?
    aIsRepeat  = db.Column(db.Boolean, nullable=False)
    # Relationship with Activity
    activityId = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    # Relationship with user bookings
    userEvents = db.relationship('UserBookings', backref='calendar')

    # Validate that date is in future
    @validates("aDateTime")
    def validate_aDateTime(self, key, Calendar):
        if Calendar < datetime.today():
            raise ValueError("Event date must be in future")
        return Calendar
    # Validates that duration is positive
    @validates("aDuration")
    def validate_aDuration(self, key, Calendar):
        if Calendar < 0:
            raise ValueError("Duration must be positive")
        return Calendar
    # Validates that price is positive
    @validates("aPrice")
    def validate_aPrice(self, key, Calendar):
        if Calendar < 0:
            raise ValueError("Price must be positive")
        return Calendar
    # Validates that capacity is positive
    @validates("aCapacity")
    def validate_aCapacity(self, key, Calendar):
        if Calendar < 0:
            raise ValueError("Capacity must be positive")
        return Calendar



class UserBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    #userId = db.Column(db.Integer, nullable=False)
    #calendarId = db.Column(db.Integer, nullable=False)

    userId = db.Column(db.Integer, db.ForeignKey('user_login.id'))
    calendarId = db.Column(db.Integer, db.ForeignKey('calendar.id'))

 
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

    # Validate that email contains @
    @validates("email")
    def validate_email(self, key, UserLogin):
        if "@" not in UserLogin:
            raise ValueError("Invalid Email")
        return UserLogin
    # Validate that user type is 1, 2 or 3
    @validates("userType")
    def validate_userType(self, key, UserLogin):
        if ((UserLogin != 1) and (UserLogin != 2) and (UserLogin != 3)):
            raise ValueError("Invalid User Type")
        return UserLogin

# User info (Sensitive info -> encryption)
class UserDetails(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # userDetailId
    name = db.Column(db.String(150), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)
    isMember = db.Column(db.Boolean)
    membershipEnd = db.Column(db.DateTime)
    paymentId=db.Column(db.String(150))
    parentId = db.Column(db.Integer, db.ForeignKey('user_login.id'))

    # Validate that age is over 16
    @validates("dateOfBirth")
    def validate_dateOfBirth(self, key, UserDetails):
        oldEnough = datetime.now().date()-timedelta(days=16*365)
        if UserDetails > oldEnough:
            raise ValueError("Not old enough")
        return UserDetails

class DiscountAmount(db.Model):
    discountAmount = db.Column(db.Integer, primary_key=True)

    @validates("discountAmount")
    def validate_discountAmount(self, key, DiscountAmount):
        maxDiscount = 100
        minDiscount = 0
        if DiscountAmount > maxDiscount or DiscountAmount < minDiscount:
            raise ValueError("Discount not within acceptable range")
        return DiscountAmount