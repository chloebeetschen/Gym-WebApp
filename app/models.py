from app import db

# table for Bookings

class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    activityType = db.Column(db.String(250))
    activityPrice = db.Column(db.Float)
    activityLocation = db.Column(db.String(250))
    activityCapacity = db.Column(db.Integer)
    activityStaffName = db.Column(db.String(250))

    #relationship with calendar
    events = db.relationship('Calendar', backref='activity_info')

class Calendar(db.Model):

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
    bookings = db.relationship('UserBookings', backref='calendar_user')

class UserBookings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    # can be added once we have the userLogin table
    # userId = db.Column(db.Integer, db.ForeignKey('UserLogin.id'))
    calendarId = db.Column(db.Integer, db.ForeignKey('calendar.id'))


