from flask import render_template, flash, request, redirect, session, url_for, g
from app import app, db
from .models import UserBookings, Calendar, Activity
from .forms import addActivityForm, addEventForm

@app.route('/')
def index():
    return '<h1>This is working.</h1>'

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
    events = Calendar.query.order_by(activityDate, activityTime).all()
    # get event info for each event found
    eventInfo = Activity.query.get(events.activityId)
    return render_template('calendar.html', title = 'Calendar', events = events, eventInfo = eventInfo)

###DONE
#this is a book event button for the calendar
@app.route('/makeBooking/<id>', methods=['GET'])
def calendarMethod(id): # << id passed here is the calendar id (not user)
    makeBooking = Calendar.get()
    #update userBookings (make one), update calendar event (increment no. of ppl and check if its full)

    #updating calendar event
    #get calendar event of id
    event = Calendar.query.get(id)
    #update number of people on current
    event.activityCurrent = event.activityCurrent + 1
    #get capactiy of that activity
    activity = Activity.query.get(event.activityId)
    #check if now it is  equal to capacity
    if event.activityCurrent == activity.activityCapacity:
        #update  fullness so that it can be represented in the table displayed
        event.activityFull == True
    

    #to update user bookings we need the user Id to be able to update for a specific user
    #for now just generically add too userBookings table where id==0
    newBooking = UserBookings(userId = 0, calendarId = id)

    #add and update db
    db.session.add(newBooking)
    db.session.commit()
        

    return redirect('/myBookings')



##DONE
#this is for the my bookings page
@app.route('/myBookings', methods=['GET', 'POST'])
def userBookingMethod():
    #need a parameter id for the user that is logged in (can be done once cookies is enabled)
    #for now we are using user of id 0
    bookings = UserBookings.query.get(0)
    #for unique user we would do
    #bookings = UserBookings.query.filter_by(currentUserId = id).all()

    # get all events in order of date and time
    events = Calendar.query.filter_by(calendarId=bookings.calendarId)
    # get event info for each event found
    eventInfo = Activity.query.get(events.activityId)
    return render_template('myBookings.html', title = 'My Bookings', events = events, eventInfo = eventInfo)

##DONE
#this is so the user is able to delete the booking - delete button
@app.route('/deleteBooking/<id>', methods=['GET'])
def deleteBooking(id): #id passed in will be  the id of the calendar
    # get the booking that matches the id of the parameter given and that of the userId (which is 0 for now)
    booking = UserBookings.filter_by(calendarId = id, userId = 0)
    # get the event in the calendar
    calendarBooking = Calendar.filter_by(id=id)
    # alter capacity of calendar
    calendarBooking.activityCurrent = calendarBooking.activityCurrent - 1
    #if was full now make bookable
    if event.activityFull:
        event.activityFull == False
    
    db.session.delete(booking)
    db.session.commit()
    return redirect('/myBookings')




##DONE
#manager add activity 
@app.route('/addActivity', methods=['POST', 'GET'])
def addActivity():
    formActivity = addActivityForm()
    #validate on submission
    if formActivity.validate_on_submission():
        #create new activity
        newAct = Activity(activityType = form.aType.data, activityPrice = form.aPrice.data, activityLocation = form.aLocation.data, activityCapacity = form.aCapacity.data, activityStaffName = form.aStaffName.data)
        #add and commit to db
        db.session.add(newAct)
        db.session.commit()

        #return to home for now
        return redirect('/')

    #if validation failed  return to add activity
    return render_template('addActivity', title = 'Add Activity', formActivity = formActivity)


##DONE
#manager add event
@app.route('/addEvent', methods=['POST', 'GET'])
def addEvent():
    formEvent = addEventForm()
    #validate on submission
    if formActivity.validate_on_submission():
        #get activity type id
        actTypeTemp = Activity.filter_by(activityType = form.type.data).first()
        #create new event
        newEvent = Calendar(activityDate = form.date.data, activityTime = form.time.data, activityDuration = form.dur.data, activityFull = False, activityCurrent = 0, activityId = actTypeTemp.id)
        #add and commit to db
        db.session.add(newEvent)
        db.session.commit()

        #return to calendar
        return redirect('/calendar')

    #if validation failed  return to add event
    return render_template('addEvent', title = 'Add Event', formEvent = formEvent)

