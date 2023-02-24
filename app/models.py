from app import db


# Login details
class UserLogin(db.Model):
    __tablename__ = "User Login"

    id = db.Column(db.Integer, primary_key=True)  # userId
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)  # Encrypt (Hash)

    child = db.relationship('User Details', backref='loginDetails', uselist=False)


# User info (Sensitive info -> encryption)
class UserDetails(db.Model):
    __tablename__ = "User Details"

    id = db.Column(db.Integer, primary_key=True)  # userDetailId
    name = db.Column(db.String(150), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(150))

    parentId = db.Column(db.Integer, db.ForeignKey('User Login.id'))
