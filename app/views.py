from app import app, db, models, admin, stripe_keys
from flask import Flask, render_template, flash, request, redirect, session, url_for, g, jsonify
from .models import *
from .forms import *
from flask_admin.contrib.sqla import ModelView
from datetime import *
from dateutil.relativedelta import relativedelta
from flask_login import current_user, login_user, LoginManager, login_required
from flask_login import logout_user
from flask_bcrypt import Bcrypt

import stripe
import logging
import random

bcrypt = Bcrypt(app)

# Register tables with flask admin
admin.add_view(ModelView(UserLogin, db.session))
admin.add_view(ModelView(UserDetails, db.session))
admin.add_view(ModelView(Calendar, db.session))
admin.add_view(ModelView(Activity, db.session))
admin.add_view(ModelView(UserBookings, db.session))

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@app.before_first_request
def deleteSessions():
    for key in list(session.keys()):
        session.pop(key)

@app.before_first_request
def addToDB():
    db.create_all()

    aDiscountExists = models.DiscountAmount.query.filter_by(discountAmount=15).first()
    if (aDiscountExists == None):
        amount = models.DiscountAmount(discountAmount=15)
        db.session.add(amount)
        db.session.commit()

    # Checks to see if the data has already been populated
    aExists = Activity.query.filter_by(activityType="Swimming (Team Events)").first()

    if (aExists == None):
        logging.debug("Creating database tables")
    
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
        today = date.today() - timedelta(days=30)
        twoWeeks = today+timedelta(days=14)

        while today < twoWeeks:
            timeStart = datetime.combine(today, time(8,00))

            #all activities in the while loop occur every day of the week
            while timeStart < datetime.combine(today, time(22,00)):
                if timeStart < datetime.combine(today, time(20,00)):
                    db.session.add_all([
                        #swimming (lane)
                        Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=10, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(2)),
                        #swimming (lessons)
                        Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=10, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(3)),
                        #swimming (general)
                        Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=10, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(4)),  
                    ])
                #climbing wall
                if timeStart > datetime.combine(today, time(10,00)):
                    db.session.add(
                        Calendar(aDateTime=timeStart, aDuration=2, aStaffName="Instructor", aPrice=10, aLocation="Climbing Wall", aCapacity=22, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(7))
                    )

                db.session.add_all([
                    #gym
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Supervisor", aPrice=5, aLocation="Fitness Room", aCapacity=35, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(5)),
                    #squash courts
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=10, aLocation="Court 1", aCapacity=4, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(6)),
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=10, aLocation="Court 2", aCapacity=4, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(6)),
                    #sports hall
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Sport Organiser", aPrice=5, aLocation="Sports Hall", aCapacity=45, aIsRepeat = True, aSlotsTaken=0, activity=Activity.query.get(12))
                ])
                
                #increment time
                timeStart = timeStart+timedelta(hours=1)

            #individual day activities
            #0 = monday ... 6 = sunday
            if today.weekday() == 0:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(18,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(8)))
            elif today.weekday() == 1:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
            elif today.weekday() == 3:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=2, aStaffName="None", aPrice=60, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(11)))
            elif today.weekday() == 4:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(10)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=80, aLocation="Swimming Pool", aCapacity=1, aIsRepeat = False, aSlotsTaken=0, activity=Activity.query.get(1)))
            elif today.weekday() == 5:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=2, aStaffName="None", aPrice=60, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(11)))
            elif today.weekday() == 6:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=80, aLocation="Swimming Pool", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(1)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(10)))


            #increment day
            today = today+timedelta(days=1)



    # Check to add daily additions:

    #get todays date and iterate for 2 weeks from today as events will appear every day
    today = date.today() - timedelta(days=30)
    twoWeeks = today+timedelta(days=14)

    while today < twoWeeks:

        timeStart = datetime.combine(today, time(8,00))
        # Check if each day has any activities:
        dayExists = Calendar.query.filter(Calendar.aDateTime >= timeStart).first()

        if( dayExists == None):
            # repeat activities:
            #all activities in the while loop occur every day of the week
            while timeStart < datetime.combine(today, time(22,00)):
                if timeStart < datetime.combine(today, time(20,00)):
                    db.session.add_all([
                        #swimming (lane)
                        Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=10, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(2)),
                        #swimming (lessons)
                        Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=10, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(3)),
                        #swimming (general)
                        Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=10, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(4)),  
                    ])
                #climbing wall
                if timeStart > datetime.combine(today, time(10,00)):
                    db.session.add(
                        Calendar(aDateTime=timeStart, aDuration=2, aStaffName="Instructor", aPrice=10, aLocation="Climbing Wall", aCapacity=22, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(7))
                    )

                db.session.add_all([
                    #gym
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Supervisor", aPrice=5, aLocation="Fitness Room", aCapacity=35, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(5)),
                    #squash courts
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=10, aLocation="Court 1", aCapacity=4, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(6)),
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=10, aLocation="Court 2", aCapacity=4, aSlotsTaken=0, aIsRepeat = True, activity=Activity.query.get(6)),
                    #sports hall
                    Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Sport Organiser", aPrice=5, aLocation="Sports Hall", aCapacity=45, aIsRepeat = True, aSlotsTaken=0, activity=Activity.query.get(12))
                ])
                
                #increment time
                timeStart = timeStart+timedelta(hours=1)

            # Individual activities:
            if today.weekday() == 0:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(18,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(8)))
            elif today.weekday() == 1:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
            elif today.weekday() == 3:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=2, aStaffName="None", aPrice=60, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(11)))
            elif today.weekday() == 4:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(10)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=80, aLocation="Swimming Pool", aCapacity=1, aIsRepeat = False, aSlotsTaken=0, activity=Activity.query.get(1)))
            elif today.weekday() == 5:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(9)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=2, aStaffName="None", aPrice=60, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(11)))
            elif today.weekday() == 6:
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=80, aLocation="Swimming Pool", aCapacity=1, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(1)))
                db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=1, aStaffName="Trainer", aPrice=5, aLocation="Studio", aCapacity=25, aSlotsTaken=0, aIsRepeat = False, activity=Activity.query.get(10)))

        #increment day
        today = today+timedelta(days=1)


    # Add admin email if doesn't exist:
    aEmailExists = UserLogin.query.filter_by(email="admin@admin.com").first()
    if (aEmailExists == None):
        hashedPassword = bcrypt.generate_password_hash('password')
        oldEnough = datetime.now().date()-timedelta(days=16*365)
        managerEmail = 'admin@admin.com'

        newUser = models.UserLogin(email=managerEmail,
                                    password=hashedPassword,
                                    userType=3)


        newUserDetails = models.UserDetails(name='Admin',
                                            dateOfBirth=oldEnough,
                                            loginDetails=newUser.id,
                                            isMember = False,
                                            membershipEnd=datetime.now())

        # Add to the database
        db.session.add(newUser)
        db.session.add(newUserDetails)

    # Add dummy data if doesn't exist:
    aEmailExists = UserLogin.query.filter_by(email="hope@nonmember.com").first()
    if (aEmailExists == None):

        hashedPassword = bcrypt.generate_password_hash('password')
        oldEnough = datetime.now().date()-timedelta(days=16*365)


        #Users without memberships 
        userEmail = 'hope@nonmember.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Hope',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = False,
                                        membershipEnd=datetime.now())
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'chloe@nonmember.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Chloe',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = False,
                                        membershipEnd=datetime.now())
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'toby@nonmember.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Toby',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = False,
                                        membershipEnd=datetime.now())
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'aaditi@nonmember.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Aaditi',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = False,
                                        membershipEnd=datetime.now())
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'gaelle@nonmember.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Gaelle',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = False,
                                        membershipEnd=datetime.now())
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'archie@nonmember.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Archie',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = False,
                                        membershipEnd=datetime.now())
        db.session.add(newUser)
        db.session.add(newUserDetails)

        #Users with memberships
        userEmail = 'hope@member.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Hope',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = True,
                                        membershipEnd=datetime.now()+timedelta(days=30))
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'chloe@member.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Chloe',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = True,
                                        membershipEnd=datetime.now()+timedelta(days=30))
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'toby@member.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Toby',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = True,
                                        membershipEnd=datetime.now()+timedelta(days=30))
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'aaditi@member.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Aaditi',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = True,
                                        membershipEnd=datetime.now()+timedelta(days=365))
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'gaelle@member.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Gaelle',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = True,
                                        membershipEnd=datetime.now()+timedelta(days=365))
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'archie@member.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=1)
        newUserDetails = models.UserDetails(name='Archie',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = True,
                                        membershipEnd=datetime.now()+timedelta(days=365))
        db.session.add(newUser)
        db.session.add(newUserDetails)


        # Employees
        userEmail = 'employee1@gymcorp.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=2)
        newUserDetails = models.UserDetails(name='Jeff',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = False,
                                        membershipEnd=datetime.now())
        db.session.add(newUser)
        db.session.add(newUserDetails)

        userEmail = 'employee2@member.com'
        newUser = models.UserLogin(email=userEmail,
                                password=hashedPassword,
                                userType=2)
        newUserDetails = models.UserDetails(name='Samantha',
                                        dateOfBirth=oldEnough,
                                        loginDetails=newUser.id,
                                        isMember = True,
                                        membershipEnd=datetime.now()+timedelta(days=365))
        db.session.add(newUser)
        db.session.add(newUserDetails)
  

        # Make bookings for users/events

        # Get all members and non members and events
        members = UserDetails.query.filter_by(isMember=True).all()
        nonMembers = UserDetails.query.filter_by(isMember=False).all() 
        events = Calendar.query.all()

        # Randomly generate bookings
        for i in range (0,50):
            event1 = random.choice(events)
            user1 = random.choice(members)
            event2 = random.choice(events)
            user2 = random.choice(nonMembers)
            if(event1.aSlotsTaken != event1.aCapacity):
                newBooking1 = UserBookings(userId = user1.id, calendarId = event1.id)
                db.session.add(newBooking1)
            if(event2.aSlotsTaken != event2.aCapacity):
                newBooking2 = UserBookings(userId = user2.id, calendarId = event2.id)
                db.session.add(newBooking2)

    db.session.commit()


@loginManager.user_loader
def loadUser(userId):
    return models.UserLogin.query.get(int(userId))
    
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/changeDiscount', methods=['GET', 'POST'])
@login_required
def changeDiscount():
    form = DiscountForm()
    if form.validate_on_submit():
        oldAmount = models.DiscountAmount.query.all()
        for amounts in oldAmount:
            db.session.delete(amounts)
            db.session.commit()
        amount = models.DiscountAmount(discountAmount=form.DiscountAmount.data)
        db.session.add(amount)
        db.session.commit()
        flash('Added new discount.', "success")
        return redirect('/home')   
    return render_template('changeDiscount.html', form=form)


# Calendar of all sessions
@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendarMethod():
    logging.debug("Calendar route request")
    today = datetime.now()

    #week span
    weeks = [today, (today + timedelta(days=1)), (today + timedelta(days=2)), (today + timedelta(days=3)), (today + timedelta(days=4)), (today + timedelta(days=5)), (today + timedelta(days=6)), (today + timedelta(days=7)), (today + timedelta(days=8)), (today + timedelta(days=9)), (today + timedelta(days=10)), (today + timedelta(days=11)), (today + timedelta(days=12)), (today + timedelta(days=13))]
    #days of week integers, from today
    
    #calculation for making sure we only get 2 weeks of data
    w1 = datetime.now()+timedelta(days=6)
    w2 = datetime.now()+timedelta(days=13)
    
    # get all events in order of date and time w1 and w2
    events1 = Calendar.query.filter(Calendar.aDateTime >= datetime.now()).filter(Calendar.aIsRepeat==False).filter(Calendar.aDateTime < w1).order_by(Calendar.aDateTime).all()
    events2 = Calendar.query.filter(Calendar.aDateTime >= w1).filter(Calendar.aDateTime < w2).filter(Calendar.aIsRepeat==False).order_by(Calendar.aDateTime).all()

    userBooked1 = []
    userBooked2 = []
    weeksCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dateWeeks = [d.date() for d in weeks]

    # get event type for each event found
    eventInfo = []
    eventPrices = []
    for i in events1:
        # Find the index of day in weeks list
        index = dateWeeks.index((i.aDateTime).date())
        weeksCount[index] +=1
        roundedPrice = "%0.2f" % i.aPrice
        eventPrices.append(roundedPrice)
        eventInfo.append(Activity.query.filter_by(id=i.activityId).first())
        # For every event check if user has booked it
        if 'proxyBooking' in session :
            for id in session['proxyBooking']:
                booked = UserBookings.query.filter_by(userId=id, calendarId=i.id).first()
        else:
            booked = UserBookings.query.filter_by(userId=current_user.id, calendarId=i.id).first()
        
        if booked is not None:   
            userBooked1.append(True)
        else:
            userBooked1.append(False)
        

    # get event type for each event found
    eventInfo2 = []
    eventPrices2 = []
    for i in events2:
        # Find the index of day in weeks list
        index = dateWeeks.index((i.aDateTime).date())
        weeksCount[index] +=1
        roundedPrice = "%0.2f" % i.aPrice
        eventPrices2.append(roundedPrice)
        eventInfo2.append(Activity.query.filter_by(id=i.activityId).first())
        # For every event check if user has booked it
        if 'proxyBooking' in session :
            for id in session['proxyBooking']:
                booked = UserBookings.query.filter_by(userId=id, calendarId=i.id).first()
        else:
            booked = UserBookings.query.filter_by(userId=current_user.id, calendarId=i.id).first()
        if booked is not None:
            userBooked2.append(True)
        else:
            userBooked2.append(False)


    if 'proxyBooking' in session :
        for id in session['proxyBooking']:
            user = UserDetails.query.filter_by(id=id).first()
    else:
        user = UserDetails.query.filter_by(id=current_user.id).first()

    if 'proxyBooking' in session:
        return render_template('calendar.html',
                            title     = 'Calendar',
                            numEvents = len(events1),
                            numEvents2 = len(events2),
                            events1    = events1,
                            eventInfo = eventInfo,
                            eventPrices = eventPrices,
                            events2    = events2,
                            eventInfo2 = eventInfo2,
                            eventPrices2 = eventPrices2,
                            isMember = True,   
                            weeks     = weeks,
                            userBooked1 = userBooked1,
                            userBooked2 = userBooked2,
                            proxyBooking = True,
                            weeksCount = weeksCount
                            )
    else:
        return render_template('calendar.html',
                            title     = 'Calendar',
                            numEvents = len(events1),
                            numEvents2 = len(events2),
                            events1    = events1,
                            eventInfo = eventInfo,
                            events2    = events2,
                            eventPrices = eventPrices,
                            eventPrices2 = eventPrices2,
                            eventInfo2 = eventInfo2,
                            isMember = user.isMember,   
                            weeks     = weeks,
                            userBooked1 = userBooked1,
                            userBooked2 = userBooked2,
                            weeksCount=weeksCount
                            )

@app.route('/calendar/<id>', methods=['GET', 'POST'])
@login_required
def proxyCustomerBooking(id):
    logging.debug("Book for a customer request")
    session['proxyBooking'] = [id]
    return redirect('/calendar')

#calendar of all repeat sessions
@app.route('/repeatEvents/<id>', methods=['GET', 'POST'])
@login_required
def repeatEvents(id):
    logging.debug("Repeat events (with id: %s) route request", id)
    week = datetime.now()+timedelta(days=14)
    events = Calendar.query.filter(Calendar.aDateTime >= datetime.now()).filter(Calendar.aDateTime < week).filter_by(activityId = id).all()
    eventType = (Activity.query.get(id)).activityType
    today = datetime.now()
    weeks = [today, (today + timedelta(days=1)), (today + timedelta(days=2)), (today + timedelta(days=3)), (today + timedelta(days=4)), (today + timedelta(days=5)), (today + timedelta(days=6)), (today + timedelta(days=7)), (today + timedelta(days=8)), (today + timedelta(days=9)), (today + timedelta(days=10)), (today + timedelta(days=11)), (today + timedelta(days=12)), (today + timedelta(days=13))]
    userBooked = []
    eventPrices = []
    for event in events:
        roundedPrice = "%0.2f" % event.aPrice
        eventPrices.append(roundedPrice)
        booked = UserBookings.query.filter_by(userId=current_user.id, calendarId=event.id).first()
        if booked is not None:   
            userBooked.append(True)
        else:
            userBooked.append(False)
    user = UserDetails.query.filter_by(id=current_user.id).first()

    if 'proxyBooking' in session:
        return render_template('repeatEvents.html',
                            title     = 'Calendar',
                            numEvents = len(events),
                            events  = events,
                            eventType = eventType,
                            eventPrices = eventPrices,
                            isMember = True,   
                            weeks     = weeks,
                            userBooked = userBooked,
                            proxyBooking = True,
                            )
    else:
        return render_template('repeatEvents.html',
                            title     = 'Calendar',
                            numEvents = len(events),
                            events  = events,
                            eventType = eventType,
                            isMember = user.isMember,   
                            weeks     = weeks,
                            userBooked = userBooked,
                            )

#this is a book event button for the calendar
@app.route('/makeBooking/<id>', methods=['GET'])
@login_required
def makeBooking(id): # << id passed here is the calendar id (not user)    
    logging.debug("Make booking (with id: %s) route request", id)    
    #update userBookings (make one), update calendar event (increment no. of ppl and check if its full)
    #updating calendar event
    #get calendar event of id
    event = Calendar.query.get(id)
    #update number of people on current
    event.aSlotsTaken += 1

    # Check if booking is for a facility with multiple events on
    if event.aLocation == "Swimming Pool" or event.aLocation == "Sports Hall":
        # If a team event, set all other swimming pool/sports hall events to full capacity for 2 hours
        if event.activityId == 1 or event.activityId == 11:
            firstHour = Calendar.query.filter_by(aDateTime=event.aDateTime, aLocation=event.aLocation).all()
            secondHour = Calendar.query.filter_by(aDateTime=event.aDateTime+timedelta(hours=1), aLocation=event.aLocation).all()
            otherEvents = firstHour + secondHour
            for events in otherEvents:
                events.aSlotsTaken = events.aCapacity
        # If not a team event, increase the slots taken for all other swimming pool events at that time
        else:
            otherEvents = Calendar.query.filter_by(aDateTime=event.aDateTime, aLocation=event.aLocation).all()
            previousHour = event.aDateTime-timedelta(hours=1)
            checkTeamEvent = Calendar.query.filter_by(aDateTime=previousHour, aLocation=event.aLocation).all()
            for events in otherEvents:
                if events.aCapacity != events.aSlotsTaken and events != event:
                    events.aSlotsTaken +=1
            for events2 in checkTeamEvent:    
                if events2.activityId == 1 or events2.activityId == 11:
                    if events2.aCapacity != events2.aSlotsTaken:
                        events2.aSlotsTaken +=1


    #get capactiy of that activity
    eventType = Activity.query.get(event.activityId)
    
    #to update user bookings we need the user Id to be able to update for a specific user
    if 'proxyBooking' in session:
        for uid in session['proxyBooking']:
            newBooking = UserBookings(userId = uid, calendarId = id)
        flash('Proxy booking completed', "success")
        for key in list(session.keys()):
            if key == 'proxyBooking':
                session.pop(key)
    else:
        newBooking = UserBookings(userId = current_user.id, calendarId = id)
    #add and update db
    db.session.add(newBooking)
    db.session.commit()
    return redirect('/myBookings')


# Add to basket button
@app.route('/addBasket/<id>', methods=['GET'])
@login_required
def addBasket(id):
    logging.debug("Add basket (with id: %s) route request", id)
    # If basket session doesn't already exist, add to session
    if 'basket' not in session:
        session['basket'] = []
    
    #First check if event is already in basket
    if id in session['basket']:
        flash("This event is already in your basket.", "error")
        return redirect('/calendar')

    # Add calendar event id to sessions
    session['basket'].append(id)
    # Flash message that event has been added to basket
    flash("An event has been added to your basket", "success")
    # Redirect back to calendar
    return redirect('/calendar')


@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket():
    logging.debug("Basket route request")
    # Boolean to store whether anything in basket
    isItems = False
    basketItems = []
    itemNames = []
    itemDiscounts = 0
    totalPrice=0
    session['basketIds'] = []

    # This is an array representing a 3 week period, 1 week before today, 2 weeks after
    datesOfBookings = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # Go through all user bookings, and if they are within one week before, or 2 weeks after, add 1 to correspoinding day count
    bookings = UserBookings.query.filter_by(userId = current_user.id)
    for booking in bookings:
        bookingEvent = Calendar.query.get(booking.calendarId)
        dayDifference = (date.today()-(bookingEvent.aDateTime).date()).days
        if (dayDifference < 7) and (dayDifference > -14):
            datesOfBookings[6-dayDifference] += 1

    # If anything in basket, set isItems to true and get all the events in basket
    if 'basket' in session:
        isItems = True
        # Go through basket adding to corresponding dates
        for id in session['basket']:
            basketEvent = Calendar.query.get(id)
            dayDifference = (date.today()-(basketEvent.aDateTime).date()).days
            if (dayDifference < 7) and (dayDifference > -14):
                datesOfBookings[6-dayDifference] += 1

        # Create list of events in basket
        for itemId in session['basket']:
            # Get item
            item = Calendar.query.get(itemId)

            # Check for discount
            discount = False
            # Go through basket items and find 7 days before

            for id in session['basket']:
                basketEvent = Calendar.query.get(id)
                dayDifference = (date.today()-(basketEvent.aDateTime).date()).days
                indexDate = 6-dayDifference
                # Count 7 days before
                count = 0
                for i in range (0, 6):
                    count += datesOfBookings[indexDate-i]
                if count > 2:
                    discount = True
                # Count 7 days after
                count = 0
                for i in range (0, 6):
                    # Check if date within 3 weeks:
                    if len(datesOfBookings) > indexDate+i:
                        count += datesOfBookings[indexDate+i]
                if count > 2:
                    discount = True
            # Change item price depending on discocunt
            if discount == True:
                amount = DiscountAmount.query.first()
                amountToDiscount = (100 - amount.discountAmount)/100
                itemPrice = item.aPrice * amountToDiscount
            else:
                itemPrice = item.aPrice
            totalPrice += itemPrice
            roundedPrice = "%0.2f" % itemPrice
            itemDiscounts += (item.aPrice - itemPrice)

            session['basketIds'].append(itemId)
            itemActivity = Activity.query.get(item.activityId)
            name = itemActivity.activityType
            nameDate = name + ", " + (item.aDateTime).strftime("%d/%m, %H:%M")
            basketItems.append((nameDate, roundedPrice))
    if 'membership' in session:
        isItems = True
        session['basketIds'].append('m')
        if session['membership'] == "monthly":
            basketItems.append(('Monthly Membership', 35))
            totalPrice += 35
        else:
            basketItems.append(("Annual Membership", 300))
            totalPrice += 300

    session['basketTotal'] = totalPrice
    # String formatting for total 2 d.p
    roundedTotal = "%0.2f" % totalPrice
    roundedDiscount = "%0.2f" % itemDiscounts
    return render_template('basket.html', title='Basket', isItems=isItems,
                            basketItems=basketItems, num=len(basketItems),
                            roundedTotal=roundedTotal, totalPrice = totalPrice,
                            roundedDiscount=roundedDiscount, key=stripe_keys['publicKey'])

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    
    user = models.UserDetails.query.filter_by(id=current_user.id).first()
    paymentId = user.paymentId

    try:
        if paymentId == None:
            customer = stripe.Customer.create(
                email=current_user.email,
                source=request.form['stripeToken']
            )

            stripe.Charge.create(
                customer=customer.id,
                amount=int(session['basketTotal']) * 100,
                currency='GBP',
                description='Push and Pull Payment'
            )
            # Save payment details for later
            user.paymentId = customer.id
            db.session.add(user)
            db.session.commit()
        else:
            stripe.Charge.create(
                customer=paymentId,
                amount=int(session['basketTotal']) * 100,
                currency='GBP',
                description='Push and Pull Payment'
            )
    except stripe.error.CardError as cardError:
        flash('Card was declined', 'error')
        return redirect('/basket')

    if 'membership' in session:
        usersDetails = UserDetails.query.get(current_user.id)
        usersDetails.isMember = True
        db.session.commit()
            
    if 'basket' in session:
        usersDetails = UserDetails.query.get(current_user.id)
        for itemId in session['basket']:
            event = Calendar.query.get(itemId)
            event.aSlotsTaken += 1
            newBooking = UserBookings(userId = current_user.id, calendarId = itemId)
            db.session.add(newBooking)
        db.session.commit()

    # Deletes all sessions after payment is completed
    for key in list(session.keys()):
        if key == 'basket':
            session.pop(key)
        if key == 'basketIds':
            session.pop(key)
        if key == 'basketTotal':
            session.pop(key)
        if key == 'membership':
            session.pop(key)

    flash('Payment Successful', "success")
    return redirect('/myBookings')

#this is so the manager is able to delete an event - delete button
@app.route('/deleteEvent/<id>', methods=['GET', 'POST'])
@login_required
def deleteEvent(id): #id passed in will be  the id of the calendar
    logging.debug("Delete event (with id: %s) route request", id)
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
    logging.debug("Delete activity route request")
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


# This is for the my bookings page
@app.route('/myBookings', methods=['GET', 'POST'])
@login_required
def myBookings():
    logging.debug("My bookings route request")
    today = datetime.now()
    # Need a parameter id for the user that is logged in (can be done once cookies is enabled)
    
    # Deletes a user's booking if the time has elapsed
    bookings = UserBookings.query.filter_by(userId=current_user.id).all()
    for booking in bookings:
        calendarEvent = booking.calendarId
        event = Calendar.query.filter_by(id=calendarEvent).first()
        eventTime = event.aDateTime
        if (eventTime <= today):
            logging.debug("Deleted booking that has completed")
            db.session.delete(booking)
            db.session.commit()    

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


@app.route('/proxyEdit/<id>', methods=['GET', 'POST'])
@login_required
def proxyEdit(id):
    session['proxyEdit'] = [id]
    return redirect(url_for('userBookings', id=id))

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
@login_required
def deleteBasket(i): # 'i' is the index of the item deleted from the basket
    logging.debug("Delete basket item (with index: %s) route request", i)
    if session['basketIds'][int(i)] == 'm':
        session.pop('membership')
    else:
        eventId = session['basketIds'][int(i)]
        session['basket'].remove(eventId)
        # Check if basket empty
        if not session['basket']:
            session.pop('basket')
        session.modified = True
    return redirect('/basket')


@app.route('/deleteBooking/<id>', methods=['GET', 'POST'])
@login_required
def deleteBooking(id): #id passed in will be  the id of the calendar
    logging.debug("Delete booking (with id: %s) route request", id)

    # get the booking that matches the id of the parameter given and that of the userId 
    
    booking = UserBookings.query.filter_by(calendarId = id, userId = current_user.id).first()

    if 'proxyEdit' in session:
        for uid in session['proxyEdit'] :
            booking = UserBookings.query.filter_by(calendarId = id, userId = uid).first()
        flash('Proxy deletion complete', "success")
        for key in list(session.keys()):
            if key == 'proxyEdit':
                session.pop(key)
    
    # get the event in the calendar
    calendarBooking = Calendar.query.filter_by(id=id).first()
    # alter capacity of calendar
    calendarBooking.aSlotsTaken -= 1

    if calendarBooking.aLocation == "Swimming Pool" or calendarBooking.aLocation == "Sports Hall":
        # First check if a team event
        if calendarBooking.activityId == 1 or calendarBooking.activityId == 11:
            # Get all events in same location for the 2 hour period
            firstHour = Calendar.query.filter_by(aDateTime=calendarBooking.aDateTime, aLocation=calendarBooking.aLocation).all()
            secondHour = Calendar.query.filter_by(aDateTime=calendarBooking.aDateTime+timedelta(hours=1), aLocation=calendarBooking.aLocation).all()
            otherEvents = firstHour + secondHour
            for event in otherEvents:
                event.aSlotsTaken = 0
        else:
            otherEvents = Calendar.query.filter_by(aDateTime=calendarBooking.aDateTime, aLocation=calendarBooking.aLocation).all()
            for event in otherEvents:
                if event.aSlotsTaken != 0 and event.activityId != 1 and event.activityId != 11 and event != calendarBooking:
                    event.aSlotsTaken -=1
            
    db.session.delete(booking)
    db.session.commit()
    return redirect('/myBookings')


#manager add activity 
@app.route('/addActivity', methods=['POST', 'GET'])
@login_required
def addActivity():
    logging.debug("Add activity route request")
    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    form = ActivityForm()
    #validate on submission
    if form.validate_on_submit():
        aExists = Activity.query.filter_by(activityType=form.aType.data).first()
        # Activity type is unique so first check that the activity doesn't exist already
        if(aExists):
            flash("This activity already exists.", "error")
            return redirect(url_for('addActivity'))

        #create new activity
        newAct = Activity(activityType=form.aType.data)

        #add and commit to db
        db.session.add(newAct)
        db.session.commit()
        flash('New activity added', "success")
    
    return render_template('addActivity.html', title='Add Activity', form=form)

#go to event edit page

#manager edit activity
@app.route('/editActivity', methods=['POST', 'GET'])
@login_required
def editActivity():
    logging.debug("Edit activity route request")
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
                flash("This activity name is already taken", "error")
                return redirect(url_for('editActivity'))
        
        # update the name with the new name
        sActivity.activityType = form.aType.data
        db.session.commit()
        flash("Updated activity type successfully", "success")

    return render_template('editActivity.html', title='Add Event',
                            form=form, activities=activities)


# manager add event
@app.route('/addEvent', methods=['POST', 'GET'])
@login_required
def addEvent():
    logging.debug("Add event route request")
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
        date = form.aDateTime.data

        cEvent = Calendar(aDateTime=date, aDuration=duration,
                          aStaffName=staff,
                          aPrice=price, aLocation=location,
                          aCapacity=capacity, aSlotsTaken=0, 
                          aIsRepeat = isRepeat, activity=sActivity)
            
        db.session.add(cEvent)
        db.session.commit()
        flash("Successfully created event!", "success")

    #if validation failed  return to add event
    return render_template('addEvent.html', title='Add Event',
                           form=form, activities=activities)



#Can this be removed it isnt being used?
#manager edit event
#for now just redirects to viewAEManager
@app.route('/editEvent/<id>', methods=['POST', 'GET'])
@login_required
def editEvent(id):
    logging.debug("Edit event (with id: %s) route request", id)
    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')

    event = Calendar.query.get(id)
    eventType = (Activity.query.get(event.activityId)).activityType
    form = EditEventForm()
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
        flash('Event edited succesfully!', "success")
        #return to previous page for now
        return redirect('/calendar')

    #if validation failed  return to add event
    return render_template('editEvent.html', title = 'Edit Event', form = form, eventType=eventType, event=event)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.debug("Login route request")
    form = LoginForm()
    if form.validate_on_submit():
        user = models.UserLogin.query.filter_by(email=form.Email.data).first()

        if user:
            # Check the password hash against the stored hashed password
            if bcrypt.check_password_hash(user.password, form.Password.data):
                login_user(user)
                if user.userType != 3:
                    return redirect(url_for('home'))
                else:
                    return redirect('/calendar')
            else:
                flash("Incorrect username/password. Please try again.", "error")
        else:
            flash("There is no account linked to this email. Please register and try again.", "error")

    return render_template('login.html', form=form, title='Login')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logging.debug("Logout route request")
    logout_user()
    # Clear sessions
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    logging.debug("Register route request")
    form = RegisterForm()

    if form.validate_on_submit():
        # Check that the email hasn't been used already.
        usedEmail = models.UserLogin.query.filter_by(email=form.Email.data).first()
        if usedEmail:
            flash("Looks like this email is already in use. Please log in.", "error")
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
                                   userType=1)

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
    isMember = False
    if current_user.is_authenticated:
        userDetail = UserDetails.query.get(current_user.id)
        if userDetail.isMember == True:
            isMember = True
        if current_user.userType == 3:
            return redirect('/calendar')
    return render_template('home.html', title='Home',
                            logged=current_user.is_authenticated,
                            isMember=isMember)



@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    logging.debug("Settings route request")
    form = SettingsForm()
    cUserDetails = models.UserDetails.query.get(current_user.id)
    if form.validate_on_submit():
        # Check the old password matches the current password
        if not bcrypt.check_password_hash(current_user.password, form.Password.data):
            flash('Incorrect password', "error")
            return redirect(url_for('settings'))

        cUserLogin   = models.UserLogin.query.get(current_user.id)
        # Only update the user's details that they have changed
        if form.Name.data:
            cUserDetails.name    = form.Name.data
        
        if form.NewPasswordx2.data:
            cUserLogin.password  = bcrypt.generate_password_hash(form.NewPassword.data)

        db.session.commit()
        flash('User Details updated', "success")

    return render_template('settings.html',
                            title='Settings',
                            form=form,
                            userIsMember=cUserDetails.isMember)

@app.route('/cancelMembership', methods=['GET', 'POST'])
@login_required
# Change user to not a member
def cancelMembership():
    logging.debug("Cancel membership route request")
    if 'proxyMembership' in session:
        for uid in session['proxyMembership']:
            usersDetails = models.UserDetails.query.get(uid)
            flash('Membership cancelled by proxy', "success")
        for key in list(session.keys()):
            if key == 'proxyMembership':
                session.pop(key)
    else:
        usersDetails = UserDetails.query.get(current_user.id)
        flash('Membership cancelled', "success")
    usersDetails.isMember = False
    usersDetails.membershipEnd = datetime.now()
    db.session.commit()
    # Redirect back to memberships page
    return redirect('/home')


@app.route('/pricingList', methods=['GET', 'POST'])
def pricingList():
    logging.debug("Pricing route request")
    return render_template('pricingList.html', title= 'Pricing List')

@app.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')


    # Get all usage and sales from past week:
    bookings = UserBookings.query.all()
    today = date.today()
    currentMemberWeek = [0,0,0,0,0,0,0]
    currentNonMemberWeek = [0,0,0,0,0,0,0]
    thisWeek = []
    currentSales = [0,0,0,0,0,0,0]
    for day in range(6, -1, -1):
        thisWeek.append( (today-timedelta(days=day)).strftime("%d/%m"))
        
        for booking in bookings:
            event = Calendar.query.filter_by(id=booking.calendarId).first()
            if event.aDateTime.date() == today-timedelta(days=day):
                user = UserDetails.query.filter_by(id=booking.userId).first()
                if user.isMember:
                    currentMemberWeek[day] += 1
                else:
                    currentNonMemberWeek[day] += 1
                    currentSales[day] += event.aPrice



    form = AnalysisForm()
    activities = Activity.query.all()
    facilities = Calendar.query.with_entities(Calendar.aLocation).distinct()

    if form.validate_on_submit():
        # Check if manager has entered facility:
        if request.form.get('facility') is not None:
            # First check that the facility exists
            facility = Calendar.query.filter_by(aLocation = request.form['facility']).first()
            if facility is None:
                flash("That is not a valid facility/location", "error")
                return redirect('/analysis')
            activityFacility = request.form['facility']
            # Get all calendar events for that location
            events = Calendar.query.filter_by(aLocation = request.form['facility']).all()

        elif request.form.get('activity') is not None:
            # First check that the activity exists
            activity = Activity.query.filter_by(activityType = request.form['activity']).first()
            if activity is None:
                flash("That is not a valid activity", "error")
                return redirect('/analysis')
            activityFacility = request.form['activity']
            # Get all calendar events for that activity
            events = Calendar.query.filter_by(activityId = activity.id).all()

        else:
            flash("Please enter either a facility or an activity", "error")
            return redirect('/analysis')

        # Get date entered
        dateEntered = form.DateOf.data
        memberWeek = [0,0,0,0,0,0,0]
        nonMemberWeek = [0,0,0,0,0,0,0]
        dates = []
        sales = [0,0,0,0,0,0,0]

        # Loop through 7 days
        for day in range(0, 7):
            dates.append( (dateEntered+timedelta(days=day)).strftime("%d/%m"))
            bookings = []
            # Get each individual booking for every event on that day
            for event in events:
                # Check for right date
                if event.aDateTime.date() == dateEntered+timedelta(days=day):
                    # Go through every user booking of events
                    for booking in event.userEvents:
                        # Add to booking
                        bookings.append(booking)
                    # Once all bookings for events have been found,
                    # it can be removed from the list of events to make future searches quicker
                    events.remove(event)

            # Now we have all user bookings for that location/activity on the right day
            # we can split them into members and non members
            for booking in bookings:
                # Check user details for each booking
                user = UserDetails.query.filter_by(id=UserBookings.userId).first()
                userMember = user.isMember
                # Increment either member or non member count
                if userMember:
                    memberWeek[day] += 1
                else:
                    # If not a member then add price to sales array
                    calendarEvent = Calendar.query.get(booking.calendarId)
                    sales[day] += calendarEvent.aPrice
                    nonMemberWeek[day] += 1

        # Set session user data
        session['activityFacility'] = activityFacility
        session['memberWeek'] = memberWeek
        session['nonMemberWeek'] = nonMemberWeek
        session['dates'] = dates
        session['sales'] = sales
        return redirect('/analysisGraphs')

    return render_template('analysis.html', title = 'Analysis', form=form, 
                            activities=activities, facilities=facilities,
                            currentNonMemberWeek=currentNonMemberWeek, 
                            currentMemberWeek=currentMemberWeek, thisWeek=thisWeek,
                            currentSales=currentSales)   

@app.route('/analysisGraphs', methods=['GET', 'POST'])
@login_required
def analysisGraphs():
    # First check the user is a manager
    if current_user.userType != 3:
        return redirect('/home')
    
    return render_template('analysisGraphs.html', title='Analysis',     activityFacility = session['activityFacility'],
                            memberWeek = session['memberWeek'], nonMemberWeek = session['nonMemberWeek'], 
                            dates = session['dates'], sales = session['sales'])




@app.route('/manageUsers', methods=['POST', 'GET'])
@login_required
def manageUsers():
    logging.debug("Manage users route request")

    # First check the user is a employee / manager
    if current_user.userType == 1:
        return redirect('/home')

    form = SearchForm()
    if form.validate_on_submit():        
        search = form.search.data
        return redirect(url_for('searchResults', search = search))

    ## Normal users
    userTypeLogin1 = UserLogin.query.filter_by(userType=1).all()

    ## Employees
    userTypeLogin2 = UserLogin.query.filter_by(userType=2).all() 

    ## Managers
    userTypeLogin3 = UserLogin.query.filter_by(userType=3).all()

   
    ## Will not render unless users of every type exist in the database
    return render_template('manageUsers.html', title = 'Manage Users', 
                            form = form,
                            userTypeNum1   = len(userTypeLogin1),
                            userTypeNum2   = len(userTypeLogin2),
                            userTypeNum3   = len(userTypeLogin3),
                            userTypeLogin1 = userTypeLogin1, 
                            userTypeLogin2 = userTypeLogin2,
                            userTypeLogin3 = userTypeLogin3,
                            userType = current_user.userType )  

## Edits a users details (name, email, password and type)
@app.route('/editUser/<id>', methods=['GET', 'POST'])
@login_required
def editUser(id):
    logging.debug("Edit user (with id: %s) route request", id)
    # First check the user is a manager
    if current_user.userType == 1:
        return redirect('/home')

    currentUserType = current_user.userType

    form = ManagerForm()
    if form.validate_on_submit():
        # Update the user's details
        cUserLogin   = models.UserLogin.query.get(id)
        cUserDetails = models.UserDetails.query.get(id)

        # Only update anything that has changed
        if form.Name.data:
            cUserDetails.name = form.Name.data
        if form.Email.data:
            cUserLogin.email = form.Email.data
        if form.NewPasswordx2.data:
            cUserLogin.password = bcrypt.generate_password_hash(form.NewPasswordx2.data)
        if form.Type.data:
            cUserLogin.userType = form.Type.data

        db.session.commit()

        flash('User Details updated', "success")
        return redirect ('/manageUsers')

        
    return render_template('editUser.html',
                            title='Edit User',
                            form=form,
                            user=id,
                            currentUserType=currentUserType)

## Deletes a user's userlogin, userdetails, userbookings and decreases the slots taken for the calender events
@app.route('/deleteUser/<id>', methods=['GET', 'POST'])
@login_required
def deleteUser(id): 
    logging.debug("Delete user (with id: %s) route request", id)
    # First check the user is a manager or employee
    if current_user.userType != 1:
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
    flash('User deleted', "success")
        
    return redirect('/manageUsers')
    
## Renders the memberships page with two options: annual and monthly
@app.route('/memberships', methods=['GET', 'POST'])
@login_required
def memberships():
    logging.debug("Memberships route request")
    # Check if user is a member
    if 'proxyMembership' in session:
        for uid in session['proxyMembership']:
            cUserDetails = models.UserDetails.query.get(uid)
    else:
        cUserDetails = models.UserDetails.query.get(current_user.id)
    isMember = cUserDetails.isMember

    return render_template('memberships.html', isMember=isMember)
 
## Adds the membership end to a month in the future
## Does not update isMember to be true as this is done after payment is completed
@app.route('/memberships/monthly', methods=['GET', 'POST'])
@login_required
def monthlyMembership():
    logging.debug("Monthly membership route request")
    if 'proxyMembership' in session:
        for uid in session['proxyMembership']:
            cUserDetails = models.UserDetails.query.get(uid)
            cUserDetails.isMember = True
            today = datetime.now()
            monthAhead = today + relativedelta(months=1)
            cUserDetails.membershipEnd = monthAhead
            db.session.commit()
            flash('Added monthly membership by proxy', "success")
            for key in list(session.keys()):
                if key == 'proxyMembership':
                    session.pop(key)
            return redirect('/home')
    else:
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
    logging.debug("Annual membership route request")
    if 'proxyMembership' in session:
        for uid in session['proxyMembership']:
            cUserDetails = models.UserDetails.query.get(uid)
            cUserDetails.isMember = True
            today = datetime.now()
            yearAhead = today + relativedelta(years=1)
            cUserDetails.membershipEnd = yearAhead
            db.session.commit()
            flash('Added monthly membership by proxy', "success")
            for key in list(session.keys()):
                if key == 'proxyMembership':
                    session.pop(key)
            return redirect('/home')
    else:
        cUserDetails = models.UserDetails.query.get(current_user.id)
        cUserDetails.isMember = False
        today = datetime.now()
        yearAhead = today + relativedelta(years=1)
        cUserDetails.membershipEnd = yearAhead
        session['membership'] = "annual" 
        db.session.commit()
        return redirect('/basket')


## search for a user
# https://stackoverflow.com/questions/39960942/flask-app-search-bar

@app.route('/searchResults/<search>', methods=['GET', 'POST'])
@login_required
def searchResults(search):

    # First check the user is a employee / manager
    if current_user.userType == 1:
        return redirect('/home')

    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        return redirect(url_for('searchResults', search = search))

    users = UserLogin.query.all()
    users2 = UserDetails.query.all()

    results = []
    for i in users:
        if search.lower() in (i.email).lower():
            results.append(i)

    for j in users2:
        if search.lower() in (j.name).lower():
            results.append(UserLogin.query.filter_by(id = j.id).first())

    results = list(dict.fromkeys(results))

    # Prevents employees from searching for manager accounts
    for user in results:
        if current_user.userType == 2:
            userSearch = UserLogin.query.filter_by(id = user.id).first()
            type = userSearch.userType
            if type == 3:
                results.remove(user)
            if type == 2:
                results.remove(user)
            

    return render_template('searches.html', 
                            title='Search Results', 
                            form = form, 
                            results = results, 
                            numUsers = len(results),
                            userType = current_user.userType)

@app.route('/proxyChangeMembership/<id>', methods=['GET', 'POST'])
@login_required
def proxyChangeMembership(id):
    session['proxyMembership'] = [id]
    return redirect('/memberships')


@app.route('/meetTheTeam')
def meetTheTeam():
    return render_template('meetTheTeam.html', title='Meet the team')

@app.route('/termsAndConditions')
def termsAndConditions():
    return render_template('termsAndConditions.html', title='Terms and Conditions')