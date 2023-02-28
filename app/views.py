from flask import render_template, flash, request, redirect, session, url_for, g
from app import app, db, models, admin
from .models import Activity, Calendar, UserBookings
from .forms import addActivityForm, addEventForm
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Calendar, db.session))
admin.add_view(ModelView(Activity, db.session))
admin.add_view(ModelView(UserBookings, db.session))


#we want 4 pages
#calendar of all sessions - and pop up for the info button
#my bookings page for the user
#manager add activity 
#manger add event 


##DONE
#calendar of all sessions
@app.route('/calendar', methods=['GET', 'POST'])
def calendarMethod():
    # get all events in order of date and time
    events = Calendar.query.order_by(Calendar.activityDate, Calendar.activityTime).all()
    # get event info for each event found
    eventInfo = []
    for i in events:
        eventInfo.append(Activity.query.filter_by(id=i.activityId).first())
    return render_template('calendar.html', title = 'Calendar', numEvents=len(events), events = events, eventInfo = eventInfo, zip=zip)

###DONE
#this is a book event button for the calendar
@app.route('/makeBooking/<id>', methods=['GET'])
def makeBooking(id): # << id passed here is the calendar id (not user)    
    #makeBooking = Calendar.get()
    #update userBookings (make one), update calendar event (increment no. of ppl and check if its full)

    #updating calendar event
    #get calendar event of id
    event = Calendar.query.get(id)
    #update number of people on current
    event.activityCurrent += + 1
    #get capactiy of that activity
    eventType = Activity.query.get(event.activityId)
    #check if now it is  equal to capacity
    if event.activityCurrent == eventType.activityCapacity:
        #update  fullness so that it can be represented in the table displayed
        event.activityFull = True
    

    #to update user bookings we need the user Id to be able to update for a specific user
    #for now just generically add too userBookings table where id==0
    newBooking = UserBookings(userId = 0, calendarId = id)

    #add and update db
    db.session.add(newBooking)
    db.session.commit()
    return redirect('/myBookings')



    

##DONE
#calendar of all sessions (manager)
@app.route('/calendarManager', methods=['GET', 'POST'])
def calendarMethodManager():
    # get all events in order of date and time
    events = Calendar.query.order_by(Calendar.activityDate, Calendar.activityTime).all()
    # get event info for each event found
    eventInfo = []
    for i in events:
        eventInfo.append(Activity.query.filter_by(id=i.activityId).first())
    return render_template('calendarManager.html', title = 'Calendar (Manager)', numEvents=len(events), events = events, eventInfo = eventInfo, zip=zip)

##DONE
#this is so the manager is able to delete an event - delete button
@app.route('/deleteEvent/<id>', methods=['GET'])
def deleteEvent(id): #id passed in will be  the id of the calendar
    # get the booking that matches the id of the parameter given and that of the userId (which is 0 for now)
    # get the event in the calendar
    
    userBs = UserBookings.query.filter_by(calendarId=id).all()
    
    for i in userBs:
        db.session.delete(i)
    
    db.session.delete(Calendar.query.get(id))
    db.session.commit()

    return redirect('/calendarManager')




##DONE
#this is for the my bookings page
@app.route('/myBookings', methods=['GET', 'POST'])
def myBookings():
    #need a parameter id for the user that is logged in (can be done once cookies is enabled)
    #for now we are using user of id 0
    bookings = UserBookings.query.filter_by(userId=0).all()
    #for unique user we would do
    #bookings = UserBookings.query.filter_by(currentUserId = id).all()

    # get all events in order of date and time
    events = []
    eventInfo = []

    for i in bookings:
        events.append(Calendar.query.filter_by(id=i.calendarId).first())
    for j in events:
        # get event info for each event found
        eventInfo.append(Activity.query.filter_by(id=j.activityId).first())


    return render_template('myBookings.html', title = 'My Bookings', numEvents=len(bookings), events = events, eventInfo = eventInfo, zip=zip)

##DONE
#this is so the user is able to delete the booking - delete button
@app.route('/deleteBooking/<id>', methods=['GET'])
def deleteBooking(id): #id passed in will be  the id of the calendar
    # get the booking that matches the id of the parameter given and that of the userId (which is 0 for now)
    booking = UserBookings.query.filter_by(calendarId = id, userId = 0).first()
    # get the event in the calendar
    calendarBooking = Calendar.query.filter_by(id=id).first()
    # alter capacity of calendar
    calendarBooking.activityCurrent -= 1
    #if was full now make bookable
    if calendarBooking.activityFull:
        calendarBooking.activityFull == False
    
    db.session.delete(booking)
    db.session.commit()
    return redirect('/myBookings')




##DONE
#manager add activity 
@app.route('/addActivity', methods=['POST', 'GET'])
def addActivity():
    form = addActivityForm()
    #validate on submission
    if form.validate_on_submit():
        # Activity type is unique so first check that the activity doesn't exist already
        if(bool(Activity.query.filter_by(activityType=form.aType.data).first())==False):
            #create new activity
            newAct = Activity(activityType = form.aType.data, activityPrice = form.aPrice.data, activityLocation = form.aLocation.data, activityCapacity = form.aCapacity.data, activityStaffName = form.aStaffName.data)
            #add and commit to db
            db.session.add(newAct)
            db.session.commit()
            flash('New activity added')
            #return to calendar for now
            return redirect('/calendar')
        else:
            # If already exists activity with same type then display error
            flash('That activity type already exists, please chose a different one')

    return render_template('addActivity.html', title = 'Add Activity', form = form)


##DONE
#manager add event
@app.route('/addEvent', methods=['POST', 'GET'])
def addEvent():
    form = addEventForm()
    #validate on submission
    if form.validate_on_submit():
        #create new event
        newEvent = Calendar(activityDate = form.cDate.data, activityTime = form.cTime.data, activityDuration = form.cDuration.data, activityFull = False, activityCurrent = 0, activityId = form.cType.data)
        #add and commit to db
        db.session.add(newEvent)
        db.session.commit()
        flash('Event succesfully added!')
        #return to same page for now
        return redirect('/addEvent')

    #if validation failed  return to add event
    return render_template('addEvent.html', title = 'Add Event', form = form)

@app.route('/')
def index():
    return redirect('/calendar')

