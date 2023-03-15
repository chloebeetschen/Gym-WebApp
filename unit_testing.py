#pair programming - Aaditi and Hope 
#used chat gpt to learn how to use unit test in python  


import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models 
from app.models import *
from flask.testing import FlaskClient 


class TestCase(unittest.TestCase):

    #this is setting up a test database 
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

       

    #this deletes the test database once testing is complete 
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    #testing the navbar - checking that correct page is loaded for its corresponding button
    #for al users
    def test_navBarAll_login(self):
        response = self.app.get(('/login'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_navBarAll_register(self):
        response = self.app.get(('/register'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)   

    def test_navBarAll_home(self):
        response = self.app.get(('/home'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)    


    #for user type 1  
    def test_navBarType1_myBookings(self):
        response = self.app.get(('/myBookings'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_navBarType1_calendar(self):
        response = self.app.get(('/calendar'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
     
    def test_navBarType1_payment(self):
        response = self.app.get(('/paymentForm'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def test_navBarType1_settings(self):
        response = self.app.get(('/settings'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    #TO DO :
    #basket / payment page 
    #pricing list page 

    #for user type 3 
    def test_navBarType2_addEvent(self):
        response = self.app.get(('/addEvent'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  

    def test_navBarType2_addActivity(self):
        response = self.app.get(('/addActivity'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  

    def test_navBarType2_viewAEManager(self):
        response = self.app.get(('/viewAEManager'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  

    def test_navBarType2_manageUsers(self):
        response = self.app.get(('/manageUsers'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  


    #registering a user and testing if this updates in the database
    def test_register(self):
        data = {
            'Name' : 'Michael Scott',
            'DateOfBirth' : '1/10/1999',
            'address' : '7 Uni Road',
            'Email' : ' michael.scott@gmail.com',
            'Password' : '12345678',
            'ReenterPassword' : '12345678'
        }
        response = self.app.post(('/register'), data=data)
        user = UserLogin.query.filter_by(email = 'michael.scott@gmail.com').first()
        self.assertIsNotNone(user)


    #testing that a registered user can log in 
    def test_login(self):
        self.user1 = UserLogin(email = 'michael.scott@gmail.com', password = '12345678', userType = '1')
        db.session.add(self.user1)
        db.session.commit()

        response = self.app.post('/login', data=dict(
            email = self.user1.email,
            password = self.user1.password,
            userType = self.user1.userType
        ), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    #logging in a user that doesn't exist
    def test_invalid_login(self):
        response = self.app.post('/login', data=dict(
            email = 'invalid',
            password = 'invalid',
            userType = 'invalid'
        ), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
    

    # #testing that if a user books an event, it shows up on their my bookings page
    # def test_bookedActivityShowsUp(self):
    #     self.user2 = UserLogin(email = 'jim.halpert@gmail.com', password = '12345678', userType = '1')
    #     db.session.add(self.user2)
    #     db.session.commit()

    #     with self.app:
    #         self.app.post('/login', data=dict(
    #             email = self.user2.email,
    #             password = self.user2.password
    #         ))

    #         #create a new activity 
    #         self.activity1 = Activity(
    #             activityType = 'Test Activity', 
    #             activityPrice = '15.00',
    #             activityLocation = 'Test loc',
    #             activityCapacity = '30',
    #             activityStaffName = 'aaditi'
    #         )
    #         db.session.add(self.activity1)
    #         db.session.commit()

    #         #book the activity 
    #         self.app.post(f'/calendar/{self.activity1.id}/makeBooking')

    #         #check if activity shows up on the user's my bookings page 
    #         response = self.app.get('/myBookings')
    #         self.assertIn(self.activity1.activityType.encode(), response.data)

    #testing that is a user cancels their booking, it is removed from their my bookings page 
