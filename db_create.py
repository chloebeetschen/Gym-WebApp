from config import SQLALCHEMY_DATABASE_URI
from app import app, models, db
from .models import *
from datetime import *    

import os.path

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.create_all()

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
                Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, activity=Activity.query.get(2)),
                #swimming (lessons)
                Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, activity=Activity.query.get(3)),
                #swimming (general)
                Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=30, aSlotsTaken=0, activity=Activity.query.get(4)),  
            ])
        #climbing wall
        if timeStart > datetime.combine(today, time(10,00)):
            db.session.add(
                Calendar(aDateTime=timeStart, aDuration=2, aStaffName="Instructor", aPrice=0, aLocation="Climbing Wall", aCapacity=22, aSlotsTaken=0, activity=Activity.query.get(7))
            )

        db.session.add_all([
            #gym
            Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Supervisor", aPrice=0, aLocation="Fitness Room", aCapacity=35, aSlotsTaken=0, activity=Activity.query.get(5)),
            #squash courts
            Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=0, aLocation="Court 1", aCapacity=4, aSlotsTaken=0, activity=Activity.query.get(6)),
            Calendar(aDateTime=timeStart, aDuration=1, aStaffName="None", aPrice=0, aLocation="Court 2", aCapacity=4, aSlotsTaken=0, activity=Activity.query.get(6)),
            #sports hall
            Calendar(aDateTime=timeStart, aDuration=1, aStaffName="Sport Organiser", aPrice=0, aLocation="Sports Hall", aCapacity=45, aSlotsTaken=0, activity=Activity.query.get(12))
        ])
        
        #increment time
        timeStart = timeStart+timedelta(hours=1)
        
    #individual day activities
    #0 = monday ... 6 = sunday
    if today.weekday() == 0:
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(18,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, activity=Activity.query.get(8)))
    elif today.weekday() == 1:
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, activity=Activity.query.get(9)))
    elif today.weekday() == 3:
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, activity=Activity.query.get(9)))
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=2, aStaffName="None", aPrice=0, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, activity=Activity.query.get(11)))
    elif today.weekday() == 4:
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(19,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, activity=Activity.query.get(10)))
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=1, aSlotsTaken=0, activity=Activity.query.get(1)))
    elif today.weekday() == 5:
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(10,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, activity=Activity.query.get(9)))
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=2, aStaffName="None", aPrice=0, aLocation="Sports Hall", aCapacity=1, aSlotsTaken=0, activity=Activity.query.get(11)))
    elif today.weekday() == 6:
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(8,00)), aDuration=2, aStaffName="Life Guard", aPrice=0, aLocation="Swimming Pool", aCapacity=1, aSlotsTaken=0, activity=Activity.query.get(1)))
        db.session.add(Calendar(aDateTime=datetime.combine(today, time(9,00)), aDuration=1, aStaffName="Trainer", aPrice=0, aLocation="Studio", aCapacity=25, aSlotsTaken=0, activity=Activity.query.get(10)))


    #increment day
    today = today+timedelta(days=1)

db.session.commit()