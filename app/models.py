from app import db

# table for Bookings

class Activity(db.Model):
    __tablename__ = "Activity"

    id = db.Column(db.Integer, primary_key=True)

    activityType = db.Column(db.String(250), primark_key=True)
    activityPrice = db.Column(db.Float)
    activityLocation = db.Column(db.String(250))
    activityCapacity = db.Column(db.Integer)
    activityStaffName = db.Column(db.String(250))

    #relationship with calendar
    events = db.relationship('Calendar', backref='activity')

class Calendar(db.Model):
    __tablename__ = "Calendar"

    id = db.Column(db.Integer, primary_key=True)

    activityDate = db.Column(db.Date, nullable=False)
    activityTime = db.Column(db.Integer, nullable=False)
    activityDuration = db.Column(db.Integer, nullable=False)
    activityFull = db.Column(db.Boolean, nullable=False)
    #this is the number of people signed up to the activity, which will need to be incremented
    activityCurrent = db.Column(db.Integer)
    
    # foreign key for activity table
    activityId = db.Column(db.Integer, db.ForeignKey('Activity.id'))

    # link to user bookings table
    bookings = db.relationship('UserBookings', backref='calendar')

class UserBookings(db.Model):
    __tablename__ = "User Bookings"

    id = db.Column(db.Integer, primary_key=True)
    
    # can be added once we have the userLogin table
    # userId = db.Column(db.Integer, db.ForeignKey('UserLogin.id'))
    calendarId = db.Column(db.Integer, db.ForeignKey('Calendar.id'))


