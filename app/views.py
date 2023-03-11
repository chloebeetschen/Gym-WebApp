from app import app, db, models, admin
from flask import Flask, render_template, flash, request, redirect, session, url_for, g
from .models import *
from .forms import *
from flask_admin.contrib.sqla import ModelView
from datetime import *

from flask_login import current_user, login_user, LoginManager, login_required
from flask_login import logout_user

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Register tables with flask admin
admin.add_view(ModelView(UserLogin, db.session))
admin.add_view(ModelView(PaymentCard, db.session))
admin.add_view(ModelView(Calendar, db.session))
admin.add_view(ModelView(Activity, db.session))
admin.add_view(ModelView(UserBookings, db.session))

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"


@app.before_first_request
def create_tables():
    db.create_all()


@loginManager.user_loader
def loadUser(userId):
    return models.UserLogin.query.get(int(userId))
    

@app.route('/')
@login_required
def index():
    # check the user type
    # If admin, show them the admin page
    return redirect(url_for('home'))


#we want 4 pages
#calendar of all sessions - and pop up for the info button
#my bookings page for the user
#manager add activity 
#manger add event 

#calendar of all sessions
@app.route('/calendar', methods=['GET', 'POST'])
def calendarMethod():
    # get all events in order of date and time
    days = datetime.now()+timedelta(days=14)
    events = Calendar.query.filter(Calendar.activityDate >= date.today()).filter(Calendar.activityDate <= days).order_by(Calendar.activityDate, Calendar.activityTime).all()
    # get event info for each event found
    eventInfo = []
    for i in events:
        eventInfo.append(Activity.query.filter_by(id=i.activityId).first())
    return render_template('calendar.html',
                            title     = 'Calendar',
                            numEvents = len(events),
                            events    = events,
                            eventInfo = eventInfo,
                            zip       = zip )

#this is a book event button for the calendar
@app.route('/makeBooking/<id>', methods=['GET'])
def makeBooking(id): # << id passed here is the calendar id (not user)    
    #makeBooking = Calendar.get()
    #update userBookings (make one), update calendar event (increment no. of ppl and check if its full)

    #updating calendar event
    #get calendar event of id
    event = Calendar.query.get(id)
    #update number of people on current
    event.activitySlotsTaken += 1
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


#calendar of all sessions (manager)
@app.route('/viewAEManager', methods=['GET', 'POST'])
def viewAEManager():
    activities = Activity.query.all()
    # get all events in order of date and time
    events = Calendar.query.order_by(Calendar.activityDate, Calendar.activityTime).all()
    # get event info for each event found
    eventInfo = []
    for i in events:
        eventInfo.append(Activity.query.filter_by(id=i.activityId).first())
    return render_template('viewAEManager.html', title = '(Manager)', activities = activities, numEvents=len(events), events = events, eventInfo = eventInfo, zip=zip)


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

    return redirect('/viewAEManager')

#something needs to be changed here
@app.route('/deleteActivity/<id>', methods=['GET'])
def deleteActivity(id): #id passed in will be  the id of the calendar
    # get the booking that matches the id of the parameter given and that of the userId (which is 0 for now)
    # get the event in the calendar
    
    actBs = Activity.query.get(id)
    calendarBs = Calendar.query.filter_by(activityId=id).all()
    #userBs = UserBookings.query.filter_by(calendarId=calendarBs.id).all()
    
    for j in calendarBs:
        userBs = UserBookings.query.filter_by(calendarId=j.id).all()
        for i in userBs:
            db.session.delete(i)
        db.session.delete(j)

    db.session.delete(actBs)
    db.session.commit() 

    return redirect('/viewAEManager')


#this is for the my bookings page
@app.route('/myBookings', methods=['GET', 'POST'])
def myBookings():
    today = date.today()
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

    return render_template('myBookings.html', title = 'My Bookings', 
                            today=today, numEvents=len(bookings),
                            events = events, eventInfo = eventInfo, zip=zip)


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


#manager add activity 
@app.route('/addActivity', methods=['POST', 'GET'])
def addActivity():
    form = addActivityForm()
    #validate on submission
    if form.validate_on_submit():

        # Activity type is unique so first check that the activity doesn't exist already
        if(bool(Activity.query.filter_by(activityType=form.aType.data).first())==False):
            #create new activity
            newAct = Activity( activityType      = form.aType.data, 
                               activityPrice     = form.aPrice.data,
                               activityLocation  = form.aLocation.data,
                               activityCapacity  = form.aCapacity.data,
                               activityStaffName = form.aStaffName.data )

            #add and commit to db
            db.session.add(newAct)
            db.session.commit()
            flash('New activity added')
            #return to calendar for now
            return redirect(url_for('addActivity'))
        else:
            # If already exists activity with same type then display error
            flash('That activity type already exists, please chose a different one')

    
    return render_template('addActivity.html', title='Add Activity', form=form)

#go to event edit page

##DONE
#manager edit activity
#for now just redirects to viewAEManager
@app.route('/editActivity/<id>', methods=['POST', 'GET'])
def editActivity(id):
    activityName = (Activity.query.get(id)).activityType
    form = editActivityForm()
    #validate on submission
    if form.validate_on_submit(): 
        edit = Calendar.query.get(id) 
        if form.aPrice.data is not None:
            edit.activityPrice = form.aPrice.data

        if form.aLocation.data is not None:
            edit.activityLocation = form.aLocation.data

        if form.aCapacity.data is not None:
            edit.activityCapacity = form.aCapacity.data

        if form.aStaffName.data is not None:
            edit.activityStaffName = form.aStaffName.data

        db.session.commit()
        flash('Activity edited succesfully!')
        # return to same page for now
        return redirect('/viewAEManager')

    # if validation failed  return to add event
    return render_template('editActivity.html', title='Add Event', form=form, activityName=activityName)


# manager add event
@app.route('/addEvent', methods=['POST', 'GET'])
@login_required
def addEvent():
    form = addEventForm()
    #validate on submission
    if form.validate_on_submit():
        # create new event
        actType = Activity.query.filter_by(activityType = form.cType.data).first()
        newEvent = Calendar(activityDate = form.cDate.data, activityTime = form.cTime.data, activityDuration = form.cDuration.data, activityFull = False, activityCurrent = 0, activityId = actType.id)
        # add and commit to db
        db.session.add(newEvent)
        db.session.commit()
        flash('Event succesfully added!')
        #return to same page for now
        return redirect('/addEvent')

    #if validation failed  return to add event
    return render_template('addEvent.html', title = 'Add Event', form = form)


#manager edit event
#for now just redirects to viewAEManager
@app.route('/editEvent/<id>', methods=['POST', 'GET'])
def editEvent(id):
    eventName = (Activity.query.get((Calendar.query.get(id)).activityId)).activityType
    form = editEventForm()
    #validate on submission
    if form.validate_on_submit(): 
        edit = Calendar.query.get(id) 
        if form.cDate.data is not None:
            edit.activityData = form.cDate.data

        if form.cTime.data is not None:
            edit.activityTime = form.cTime.data

        if form.cDuration.data is not None:
            edit.activityDuration = form.cDuration.data

        db.session.commit()
        flash('Event edited succesfully!')
        #return to same page for now
        return redirect('/viewAEManager')

    #if validation failed  return to add event
    return render_template('editEvent.html', title = 'Add Event', form = form, eventName=eventName)


#Payment Form page
@app.route('/paymentForm', methods=['GET', 'POST'])
def paymentForm():
    form = PaymentForm()
    
    # Add data to database on submit:
    if form.validate_on_submit():
        # Create Payment Card field with entered details
        newCard = models.PaymentCard( cardName    = form.cName.data,
                                      cardNum     = form.cNum.data,
                                      cardExpDate = form.cExpDate.data,
                                      cardCVV     = form.cCVV.data )

        # Add new card entry to database and commit
        db.session.add(newCard)
        db.session.commit()

        flash('Payment details registered')
    return render_template('paymentForm.html', title='Payment Form', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = models.UserLogin.query.filter_by(email=form.Email.data).first()

        if user:
            # Check the password hash against the stored hashed password
            if bcrypt.check_password_hash(user.password, form.Password.data):
                login_user(user)
                return redirect(url_for('home'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check that the email hasn't been used already.
        usedEmail = models.UserLogin.query.filter_by(email=form.Email.data).first()
        if usedEmail:
            flash("Looks like this email is already in use. Please log in.")
            return redirect(url_for('login'))

        # Get data from the form
        Name    = form.Name.data
        dob     = form.DateOfBirth.data
        Address = form.Address.data
        Email   = form.Email.data
        
        hashedPassword = bcrypt.generate_password_hash(form.Password.data)

        # Create new user and details
        # users that register are automatically set to 1
        newUser = models.UserLogin(email=Email,
                                   password=hashedPassword,
                                   userType=form.Type.data)
        newUserDetails = models.UserDetails(name=Name,
                                            dateOfBirth=dob,
                                            address=Address,
                                            loginDetails=newUser.id)

        # Add to the database
        db.session.add(newUser)
        db.session.add(newUserDetails)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title="Register")


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='home')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        # Check the old password matches the current password
        if not bcrypt.check_password_hash(current_user.password, form.Password.data):
            flash('Incorrect password')
            return redirect(url_for('settings'))
        # Update the user's details
        cUserLogin   = models.UserLogin.query.get(current_user.id)
        cUserDetails = models.UserDetails.query.get(current_user.id)

        cUserDetails.name    = form.Name.data
        cUserDetails.address = form.Address.data
        cUserLogin.password  = bcrypt.generate_password_hash(form.NewPassword.data)

        db.session.commit()
        flash('User Details updated')
        
    return render_template('settings.html',
                            title='Settings',
                            form=form,
                            user=current_user)

@app.route('/memberships', methods=['GET', 'POST'])
@login_required
def memberships():

    ####### NOT CURRENTLY WORKING #######
    form = MembershipForm()
    if form.validate_on_submit():
        cUserLogin   = models.UserLogin.query.get(current_user.id)
        cUserDetails = models.UserDetails.query.get(current_user.id)
        cUserDetails.membershipStart = form.MembershipStart
        cUserDetails.membershipEnd = form.MembershipEnd
        return redirect('/paymentForm/memberships')
    #####################################
    
    return render_template('memberships.html', form=form)
 
    
#Payment Form for memberships page
@app.route('/paymentForm/memberships', methods=['GET', 'POST'])
@login_required
def paymentMembershipsForm():
    return redirect('/settings')
