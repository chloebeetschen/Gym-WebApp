from app import db

# table for Bookings
class UserBookings(db.Model):
    __tablename__ = "User Bookings"

    id = db.Column(db.Integer, primary_key=True)
    
    userId = db.Column(db.Integer, db.ForeignKey('UserLogin.id'))
    calendarId = db.Column(db.Integer, db.ForeignKey('Calendar.id'))


class Calendar(db.Model):
    __tablename__ = "Calendar"

    id = db.Column(db.Integer, primary_key=True)

    activityDate = db.Column(db.Date, nullable=false)
    activityTime = db.Column(db.Integer, nullable=false)
    activityDuration = d.Column(db.Integer, nullable=false)
    activityFull = db.Column(db.Boolean, nullable=false)
    #this is the number of people signed up to the activity, which will need to be incremented
    activityCurrent = db.Column(db.Integer)
    activityId = db.Column(db.Integer, db.ForeignKey('Activity.id'))


class Activity(db.Model):
    __tablename__ = "Activity"

    id = db.Column(db.Integer, primary_key=True)

    activityType = db.Column(db.String(250), primark_key=true)
    activityPrice = db.Column(db.Float)
    activityLocation = db.Column(db.String(250))
    activityCapacity = db.Column(db.Integer)
    activityStaffName = db.Column(db.String(250))