from app import db
from flask_login import UserMixin


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