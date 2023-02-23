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


#calendar of all sessions
@app.route('/calendar', methods=['GET', 'POST'])
def calendarMethod():
    #would need to check if session  is full and alter colours/ if button can be clicked
    events = Calendar.query.all()
    return render_template('calendar.html', title = 'Calendar', events = events)

#this is a book event button for the calendar
@app.route('/makeBooking/<id>', methods=['GET'])
def calendarMethod(id):
    makeBooking = Calendar.get()
    #update userBookings (make one), update calendar event (increment no. of ppl and check if its full)

    return redirect('/myBookings')




#this is for the my bookings page
@app.route('/myBookings', methods=['GET', 'POST'])
def userBookingMethod(): #parameter is id for the user that is logged in (can be done once cookies is enabled)
    bookings = UserBookings.query.all()
    #the above statement is for all bookings that have been made
    #for unique user
    #bookings = UserBookings.query.filter_by(currentUserId = id).all()
    return render_template('myBookings.html', title = 'My Bookings', bookings = bookings)


#this is so the user is able to delete the booking - delete button
@app.route('/deleteBooking/<id>', methods=['GET'])
def deleteBooking(id):
    booking = UserBookings.get(id)
    db.session.delete(booking)
    db.session.commit
    return redirect('/myBookings')





#manager add activity 
@app.route('/addActivity', methods=['POST', 'GET'])
def addActivity():
    formActivity = addActivityForm()
    #validate on submission

    return render_template('addActivity', title = 'Add Activity', formActivity = formActivity)



#manager add event
@app.route('/addEvent', methods=['POST', 'GET'])
def addEvent():
    formEvent = addEventForm()
    #validate on submission

    return render_template('addEvent', title = 'Add Event', formEvent = formEvent)

