from app import app, db, models, admin
from flask import Flask, render_template, flash, request, redirect, session, url_for, g
from .models import *
from .forms import *
from flask_admin.contrib.sqla import ModelView
from datetime import *
from dateutil.relativedelta import relativedelta

from flask_login import current_user, login_user, LoginManager, login_required
from flask_login import logout_user

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Register tables with flask admin
admin.add_view(ModelView(UserLogin, db.session))
admin.add_view(ModelView(UserDetails, db.session))
admin.add_view(ModelView(PaymentCard, db.session))
admin.add_view(ModelView(Calendar, db.session))
admin.add_view(ModelView(Activity, db.session))
admin.add_view(ModelView(UserBookings, db.session))

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@app.before_first_request
def delete_sessions():
    for key in list(session.keys()):
        session.pop(key)

'''
@app.before_first_request
def create_tables():
    db.create_all()
    
    #pre-populating calendar and activity with given data from spec

    db.session.add_all([
        Activity(activityType="Swimming (Team Events)"),    #1
        Activity(activityType="Swimming (Lane Swimming)"),  #2
        Activity(activityType="Swimming (Lessons)"),        #3 
        Activity(activityType="Swimming (General Use)"),    #4
        Activity(activityType="Gym"),                       #5
        Activity(activityType="Squash"),                    #6
        Activity(activityType="Climbing"),                  #7
        Activity(activityType="Pilates"),                   #8
        Activity(activityType="Aerobics"),                  #9
        Activity(activityType="Yoga"),                      #10
        Activity(activityType="Sports Hall (Team Events)"), #11
        Activity(activityType="Sports Hall (Session)")      #12
    ])

    #get todays date and iterate for 2 weeks from today as events will appear every day
    today = date.today() + timedelta(days=1)
    twoWeeks = today+timedelta(days=14)

    while today < twoWeeks:
        timeStart = datetime.combine(today, time(8,00))

        #all activities in the while loop occur every day of the week
        while timeStart < datetime.combine(today, time(22,00)):
            if timeStart < datetime.combine(today, time(20,00)):
                db.session.add_all([
                    #swimming (lane)
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(2)),
                    #swimming (lessons)
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(3)),
                    #swimming (general)
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(4)),  
                ])
            #climbing wall
            if timeStart > datetime.combine(today, time(10,00)):
                db.session.add(
                    Calendar(aDateTime=timeStart, aDuration=2, aStaffName="Instructor", aPrice=0, aLocation="Climbing Wall", aCapacity=22, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(7))
                )

            db.session.add_all([
                #gym
                Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Supervisor", aPrice=0, aLocation="Fitness Room", aCapacity=35, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(5)),
                #squash courts
                Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=0, aLocation="Court 1", aCapacity=4, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(6)),
                Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=0, aLocation="Court 2", aCapacity=4, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(6)),
                #sports hall
                Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Sport Organiser", aPrice=0, aLocation="Sports Hall", aCapacity=45, aIsRepeat = True, aSlotsTaken=0, activity=Activity.query.get(12))
            ])
            
            #increment time
            timeStart = timeStart+timedelta(hours=1)
            
        #individual day activities
        #0 = monday ... 6 = sunday
        if today.weekday() == 0:
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(18,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(8)))
        elif today.weekday() == 1:
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
        elif today.weekday() == 3:
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=2, aStaffName="None", aPrice=0, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(11)))
        elif today.weekday() == 4:
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(10)))
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=1, aIsRepeat = False, aSlotsTaken=0, activity=Activity.query.get(1)))
        elif today.weekday() == 5:
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=2, aStaffName="None", aPrice=0, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(11)))
        elif today.weekday() == 6:
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(1)))
            db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(10)))


        #increment day
        today = today+timedelta(days=1)

    db.session.commit()
'''

@loginManager.user_loader
def loadUser(userId):
    return models.UserLogin.query.get(int(userId))
    

@app.route('/')
@login_required
def index():
    return redirect(url_for('home'))


# Calendar of all sessions
@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendarMethod():
    today = datetime.now()
    #week span
    weeks = [today, (today + timedelta(days=1)), (today + timedelta(days=2)), (today + timedelta(days=3)), (today + timedelta(days=4)), (today + timedelta(days=5)), (today + timedelta(days=6)), (today + timedelta(days=7)), (today + timedelta(days=8)), (today + timedelta(days=9)), (today + timedelta(days=10)), (today + timedelta(days=11)), (today + timedelta(days=12)), (today + timedelta(days=13))]
    #days of week integers, from today
    
    #array for constant events
    #dailyConstantEvents = ["Swimming (Lane Swimming)", "Swimming (General Use)", "Gym", "Swimming (Lessons)", "Squash", "Sports Hall (Session)", "Climbing"]
    
    #calculation for making sure we only get 2 weeks of data
    w1 = datetime.now()+timedelta(days=7)
    w2 = datetime.now()+timedelta(days=14)
    # get all events in order of date and time w1 and w2
    events = Calendar.query.filter(Calendar.aDateTime >= date.today()).filter(Calendar.aDateTime < w1).filter_by(aIsRepeat = False).order_by(Calendar.aDateTime).all()
    events2 = Calendar.query.filter(Calendar.aDateTime >= w1).filter(Calendar.aDateTime < w2).filter_by(aIsRepeat = False).order_by(Calendar.aDateTime).all()

    # get event type for each event found
    eventInfo = []
    for i in events:
        eventInfo.append(Activity.query.filter_by(id=i.activityId).first())

    # get event type for each event found
    eventInfo2 = []
    for i in events2:
        eventInfo2.append(Activity.query.filter_by(id=i.activityId).first())


    user = UserDetails.query.filter_by(id=current_user.id).first()
    print(user)
    
    return render_template('calendar.html',
                            title     = 'Calendar',
                            numEvents = len(events),
                            numEvents2 = len(events2),
                            events    = events,
                            eventInfo = eventInfo,
                            events2    = events2,
                            eventInfo2 = eventInfo2,
                            isMember = user.isMember,   
                            weeks     = weeks)

#calendar of all repeat sessions
@app.route('/repeatEvents/<id>', methods=['GET', 'POST'])
def repeatEvents(id):

    week = datetime.now()+timedelta(days=7)
    events = Calendar.query.filter(Calendar.aDateTime >= date.today()).filter(Calendar.aDateTime < week).filter_by(activityId = id).all()
    eventType = (Activity.query.get(id)).activityType
    
    today = datetime.now()
    weeks = [today, (today + timedelta(days=1)), (today + timedelta(days=2)), (today + timedelta(days=3)), (today + timedelta(days=4)), (today + timedelta(days=5)), (today + timedelta(days=6)), (today + timedelta(days=7)), (today + timedelta(days=8)), (today + timedelta(days=9)), (today + timedelta(days=10)), (today + timedelta(days=11)), (today + timedelta(days=12)), (today + timedelta(days=13))]

    user = UserDetails.query.filter_by(id=current_user.id).first()




    return render_template('repeatEvents.html',
                            title     = 'Calendar of Constant Events',
                            numEvents = len(events),
                            events    = events,
                            eventType = eventType,
                            member    = user.isMember,
                            weeks     = weeks)

#this is a book event button for the calendar
@app.route('/makeBooking/<id>', methods=['GET'])
def makeBooking(id): # << id passed here is the calendar id (not user)    
    
    #update userBookings (make one), update calendar event (increment no. of ppl and check if its full)

    #updating calendar event
    #get calendar event of id
    event = Calendar.query.get(id)
    #update number of people on current
    event.aSlotsTaken += 1
    #get capactiy of that activity
    eventType = Activity.query.get(event.activityId)
    
    #to update user bookings we need the user Id to be able to update for a specific user
    newBooking = UserBookings(userId = current_user.id, calendarId = id)

    #add and update db
    db.session.add(newBooking)
    db.session.commit()
    return redirect('/myBookings')


# Add to basket button
@app.route('/addBasket/<id>', methods=['GET'])
def addBasket(id):
    # If basket session doesn't already exist, add to session
    if 'basket' not in session:
        session['basket'] = []
    # Add calendar event id to sessions
    session['basket'].append(id)
    # Flash message that event has been added to basket
    flash("An event has been added to your basket")
    # Redirect back to calendar
    return redirect('/calendar')

@app.route('/basket', methods=['GET', 'POST'])
def basket():
    # Boolean to store whether anything in basket
    isItems = False
    basketItems = []
    itemNames = []
    totalPrice=0
    session['basketIds'] = []
    
    # If anything in basket, set isItems to true and get all the events in basket
    if 'basket'in session:
        isItems = True
        # Create list of events in basket
        for itemId in session['basket']:
            item = Calendar.query.get(itemId)
            totalPrice += item.aPrice
            session['basketIds'].append(itemId)
            itemActivity = Activity.query.get(item.activityId)
            name = itemActivity.activityType
            nameDate = name + ", " + (item.aDateTime).strftime("%d/%m, %H:%M")
            basketItems.append((nameDate, item.aPrice ))

    if 'membership' in session:
        isItems = True
        session['basketIds'].append('m')
        if session['membership'] == "monthly":
            basketItems.append(('Monthly Membership', 35))
            totalPrice += 35
        else:
            basketItems.append(("Annual Membership", 300))
            totalPrice += 300

    return render_template('basket.html', title='Basket', isItems=isItems, basketItems=basketItems, num=len(basketItems), totalPrice=totalPrice)

#this is so the manager is able to delete an event - delete button
@app.route('/deleteEvent/<id>', methods=['GET', 'POST'])
@login_required
def deleteEvent(id): #id passed in will be  the id of the calendar

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

        
    # get the booking that matches the id of the parameter given and that of the userId (which is 0 for now)
    # get the event in the calendar
    userBs = UserBookings.query.filter_by(userId=current_user.id).filter_by(calendarId=id).all()
    
    for i in userBs:
        db.session.delete(i)
    
    db.session.delete(Calendar.query.get(id))
    db.session.commit()

    return redirect('/calendar')

#needs fully checking but up to date
@app.route('/deleteActivity', methods=['GET', 'POST'])
@login_required
def deleteActivity(): 

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    # Should delete the activity(today + timedelta(days=1)), (today + timedelta(days=2)), (today + timedelta(days=3)), (today + timedelta(days=4)), (today + timedelta(days=5)), ((today + timedelta(days=6))
    sActivity = models.Activity.query.filter_by(activityType=request.form['activity']).first()  # The activity selected

    #get all calendar events containing the activity
    allEvents = Calendar.query.filter_by(activityId = sActivity.id).all()

    #get all user bookings with the calendar id of any of the calendarIds in allEvents and delete
    for i in allEvents:
        userEvents = UserBookings.query.filter_by(calendarId = i.id).all()
        for j in userEvents:
            db.session.delete(j)
        db.session.delete(i)
    
    db.session.delete(sActivity)
    db.session.commit()
    
    return redirect('/editActivity')


#this is for the my bookings page
@app.route('/myBookings', methods=['GET', 'POST'])
@login_required
def myBookings():
    today = datetime.now()
    #need a parameter id for the user that is logged in (can be done once cookies is enabled)
    bookings = UserBookings.query.filter_by(userId=current_user.id).all()

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
                            events = events, eventInfo = eventInfo)

@app.route('/userBookings/<id>', methods=['GET', 'POST'])
@login_required
def userBookings(id):
    today = datetime.now()
    #need a parameter id for the user that is logged in (can be done once cookies is enabled)
    bookings = UserBookings.query.filter_by(userId=id).all()

    # get all events in order of date and time
    events = []
    eventInfo = []

    for i in bookings:
        events.append(Calendar.query.filter_by(id=i.calendarId).first())

    for j in events:
        # get event info for each event found
        eventInfo.append(Activity.query.filter_by(id=j.activityId).first())

    return render_template('myBookings.html', title = 'Bookings', 
                            today=today, numEvents=len(bookings),
                            events = events, eventInfo = eventInfo)


@app.route('/deleteBasket/<i>', methods=['GET'])
def deleteBasket(i): # 'i' is the index of the item deleted from the basket
    if session['basketIds'][int(i)] == 'm':
        session.pop('membership')
    else:
        eventId = session['basketIds'][int(i)]
        print(eventId)
        print(session['basket'])
        session['basket'].remove(eventId)
        print(session['basket'])
        # Check if basket empty
        if not session['basket']:
            session.pop('basket')
    return redirect('/basket')
    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

@app.route('/deleteBooking/<id>', methods=['GET'])
def deleteBooking(id): #id passed in will be  the id of the calendar
    # get the booking that matches the id of the parameter given and that of the userId 
    booking = UserBookings.query.filter_by(calendarId = id, userId = current_user.id).first()
    # get the event in the calendar
    calendarBooking = Calendar.query.filter_by(id=id).first()
    # alter capacity of calendar
    calendarBooking.aSlotsTaken -= 1
    
    db.session.delete(booking)
    db.session.commit()
    return redirect('/myBookings')


#manager add activity 
@app.route('/addActivity', methods=['POST', 'GET'])
def addActivity():

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    form = ActivityForm()
    #validate on submission
    if form.validate_on_submit():
        aExists = Activity.query.filter_by(activityType=form.aType.data).first()
        # Activity type is unique so first check that the activity doesn't exist already
        if(aExists):
            flash("This activity already exists.")
            return redirect(url_for('addActivity'))

        #create new activity
        newAct = Activity(activityType=form.aType.data)

        #add and commit to db
        db.session.add(newAct)
        db.session.commit()
        flash('New activity added')
    
    return render_template('addActivity.html', title='Add Activity', form=form)

#go to event edit page

#manager edit activity
@app.route('/editActivity', methods=['POST', 'GET'])
@login_required
def editActivity():

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    form = ActivityForm()
    activities = Activity.query.all()  # Get all activities
    if form.validate_on_submit():
        sActivity = Activity.query.filter_by(activityType=request.form['activity']).first()  # The activity selected

        # Check the new name isn't the same as any of the other names
        for activity in activities:
            if form.aType.data.upper() == activity.activityType.upper():
                flash("This activity name is already taken")
                return redirect(url_for('editActivity'))
        
        # update the name with the new name
        sActivity.activityType = form.aType.data
        db.session.commit()
        flash("Updated activity type successfully")

    return render_template('editActivity.html', title='Add Event',
                            form=form, activities=activities)


# manager add event
@app.route('/addEvent', methods=['POST', 'GET'])
@login_required
def addEvent():

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    form = EventForm()
    activities = Activity.query.all()

    if form.validate_on_submit():
        # Make a new calendar event with the data in the form
        sActivity = models.Activity.query.filter_by(activityType=request.form['activity']).first()  # The activity selected
        
        # Get data from the form
        duration = form.aDuration.data
        staff    = form.aStaffName.data
        location = form.aLocation.data
        price    = form.aPrice.data
        capacity = form.aCapacity.data
        isRepeat = False

        # y, m, d = form.aDate.data.split('-')
        # date = datetime.datetime(int(y), int(m), int(d))
        print(type(form.aDateTime.data))
        date = form.aDateTime.data

        cEvent = Calendar(aDateTime=date, aDuration=duration,
                          aStaffName=staff,
                          aPrice=price, aLocation=location,
                          aCapacity=capacity, aSlotsTaken=0, 
                          aIsRepeat = isRepeat, activity=sActivity)
            
        db.session.add(cEvent)
        db.session.commit()
        flash("Successfully created event!")

    #if validation failed  return to add event
    return render_template('addEvent.html', title='Add Event',
                           form=form, activities=activities)



#Can this be removed it isnt being used?
#manager edit event
#for now just redirects to viewAEManager
@app.route('/editEvent/<id>', methods=['POST', 'GET'])
@login_required
def editEvent(id):

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    event = Calendar.query.get(id)
    eventType = (Activity.query.get(event.activityId)).activityType
    form = EventForm()
    #validate on submission
    if form.validate_on_submit(): 
        if form.aDateTime.data is not None:
            event.aDateTime = form.aDateTime.data

        if form.aDuration.data is not None:
            event.aDuration = form.aDuration.data

        if form.aStaffName.data is not None:
            event.aStaffName = form.aStaffName.data

        if form.aLocation.data is not None:
            event.aLocation = form.aLocation.data
        
        if form.aPrice.data is not None:
            event.aPrice = form.aPrice.data

        if form.aCapacity.data is not None:
            event.aCapacity = form.aCapacity.data

        db.session.commit()
        flash('Event edited succesfully!')
        #return to previous page for now
        return redirect('/calendar')

    #if validation failed  return to add event
    return render_template('editEvent.html', title = 'Edit Event', form = form, eventType=eventType, event=event)

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
    # Clear sessions
    for key in list(session.keys()):
        session.pop(key)
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
        Email   = form.Email.data

        
        hashedPassword = bcrypt.generate_password_hash(form.Password.data)

        # Create new user and details
        # users that register are automatically set to 1
        newUser = models.UserLogin(email=Email,
                                   password=hashedPassword,
                                   userType=form.Type.data)

        newUserDetails = models.UserDetails(name=Name,
                                            dateOfBirth=dob,
                                            loginDetails=newUser.id,
                                            isMember = False,
                                            membershipEnd=datetime.now())

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
        cUserLogin.password  = bcrypt.generate_password_hash(form.NewPassword.data)

        db.session.commit()
        flash('User Details updated')
        
    return render_template('settings.html',
                            title='Settings',
                            form=form,
                            user=current_user)

@app.route('/cancelMembership', methods=['GET', 'POST'])
@login_required
def cancelMembership():
    # Change user to not a member
    usersDetails = UserDetails.query.get(current_user.id)
    usersDetails.isMember = False
    usersDetails.membershipEnd = datetime.now()
    db.session.commit()
    # Redirect back to memberships page
    return redirect('/memberships')


@app.route('/pricingList', methods=['GET', 'POST'])
def pricingList():
    return render_template('pricingList.html', title= 'Pricing List')

@app.route('/manageUsers', methods=['POST', 'GET'])
@login_required
def manageUsers():

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    ## Normal users
    userTypeLogin1 = UserLogin.query.filter_by(userType=1).all()

    ## Employees
    userTypeLogin2 = UserLogin.query.filter_by(userType=2).all() 

    ## Managers
    userTypeLogin3 = UserLogin.query.filter_by(userType=3).all()

   
    ## Will not render unless users of every type exist in the database
    return render_template('manageUsers.html', title = 'Manage Users', 
                            userTypeNum1   = len(userTypeLogin1),
                            userTypeNum2   = len(userTypeLogin2),
                            userTypeNum3   = len(userTypeLogin3),
                            userTypeLogin1 = userTypeLogin1, 
                            userTypeLogin2 = userTypeLogin2,
                            userTypeLogin3 = userTypeLogin3 )  

## Edits a users details (name, email, password and type)
@app.route('/editUser/<id>', methods=['GET', 'POST'])
@login_required
def editUser(id):

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    form = ManagerForm()
    if form.validate_on_submit():
        # Update the user's details
        cUserLogin   = models.UserLogin.query.get(id)
        cUserDetails = models.UserDetails.query.get(id)

        cUserDetails.name    = form.Name.data
        cUserLogin.email     = form.Email.data
        cUserLogin.password  = bcrypt.generate_password_hash(form.NewPasswordx2.data)
        cUserLogin.userType      = form.Type.data

        db.session.commit()
        flash('User Details updated')
        
    return render_template('editUser.html',
                            title='Edit User',
                            form=form,
                            user=id)

## Deletes a user's userlogin, userdetails, userbookings and decreases the slots taken for the calender events
@app.route('/deleteUser/<id>', methods=['GET', 'POST'])
@login_required
def deleteUser(id): 

    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    cUserLogin   = models.UserLogin.query.get(id)

    ## Slightly problematic - should be getting parentId, but works as there shouldn't be a situation where 
    ## userdetails.id is different from parentid
    cUserDetails = models.UserDetails.query.get(id)
    
    cUserBookings = models.UserBookings.query.filter_by(userId = id).all()

    for item in cUserBookings:
        event = Calendar.query.get(item.calendarId)
        event.aSlotsTaken -= 1
        db.session.delete(item)


    db.session.delete(cUserLogin)
    db.session.delete(cUserDetails)

    db.session.commit()
    flash('User deleted')
        
    return render_template('home.html',
                            title='Home')

## Renders the memberships page with two options: annual and monthly
@app.route('/memberships', methods=['GET', 'POST'])
@login_required
def memberships():
    # Check if user is a member
    cUserDetails = models.UserDetails.query.get(current_user.id)
    isMember = cUserDetails.isMember

    return render_template('memberships.html', isMember=isMember)
 
## Adds the membership end to a month in the future
## Does not update isMember to be true as this is done after payment is completed
@app.route('/memberships/monthly', methods=['GET', 'POST'])
@login_required
def monthlyMembership():
    cUserDetails = models.UserDetails.query.get(current_user.id)
    cUserDetails.isMember = False
    today = datetime.now()
    monthAhead = today + relativedelta(months=1)
    cUserDetails.membershipEnd = monthAhead
    session['membership'] = "monthly"
    db.session.commit()
    ##Test to see if working correctly
    return redirect('/basket')

## Adds the membership end to a year in the future
## Does not update isMember to be true as this is done after payment is completed
@app.route('/memberships/annual', methods=['GET', 'POST'])
@login_required
def annualMembership():
    cUserDetails = models.UserDetails.query.get(current_user.id)
    cUserDetails.isMember = False
    today = datetime.now()
    yearAhead = today + relativedelta(years=1)
    cUserDetails.membershipEnd = yearAhead
    session['membership'] = "annual"
   
    db.session.commit()
    ##Test to see if working correctly
    return redirect('/basket')
