#pair programming - Aaditi and Hope 
#used chat gpt to learn how to use unit test in python  


import unittest
from flask import Flask, current_app, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models 
from app.models import *
from app.views import *
from app.forms import *
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

    def test_navBarAll_register(self):
        response = self.app.get(('/register'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)   

    def test_navBarAll_home(self):
        response = self.app.get(('/home'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)   

    def test_navBarAll_login(self):
        response = self.app.get(('/login'), follow_redirects = True)
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

    def test_navBarType1_basket(self):
        response = self.app.get(('/basket'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
    
    def test_navBarType1_memberships(self):
        response = self.app.get(('/memberships'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)   
            
    #TO DO :
    #pricing list page 

    #for user type 3 
    def test_navBarType2_addEvent(self):
        response = self.app.get(('/addEvent'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  

    def test_navBarType2_addActivity(self):
        response = self.app.get(('/addActivity'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)   

    def test_navBarType2_manageUsers(self):
        response = self.app.get(('/manageUsers'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  


    #registering a user and testing if this updates in the database
    def test_register(self):
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

        with app.test_request_context():
            with app.app_context():
                data = {
                    'Name' : 'Michael Scott',
                    'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                    'Address' : '7 Uni Road',
                    'Email' : 'michael.scott@gmail.com',
                    'Password' : '12345678',
                    'ReenterPassword' : '12345678',
                    'Type' : 1
                    }

                form = RegisterForm(data=data)
                self.assertTrue(form.validate())
                if not form.validate():
                    print(form.errors)

                response = self.app.post('/register', data=data)
                
                #user = models.UserDetails.query.filter_by(name= 'Michael Scott').first()
                user = models.UserLogin.query.filter_by(email= 'michael.scott@gmail.com').first()
                self.assertIsNotNone(user)


    #testing to see if we can register a user with missing details - should not be able to
    #missing email field 
    def test_registerMissing(self):
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

        with app.test_request_context():
            with app.app_context():
                data = {
                'Name' : 'Pam Halpert',
                'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                'Address' : '89 Uni Road',
                'Email' : ' ',
                'Password' : '12345678',
                'ReenterPassword' : '12345678',
                'Type' : 1
                }

                form = RegisterForm(data=data)
                #form should not be valid since there is missing data
                self.assertFalse(form.validate())
                error_dict = form.errors
                #check if error message for missing email is displayed
                self.assertIn('Please enter an email', error_dict.get('Email', []))

    
    #testing to see if we can register a user with missing details - should not be able to
    #missing Name field 
    def test_registerMissing(self):
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

        with app.test_request_context():
            with app.app_context():
                data = {
                'Name' : ' ',
                'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                'Address' : '89 Uni Road',
                'Email' : 'Pam.halpert@gmail.com',
                'Password' : '12345678',
                'ReenterPassword' : '12345678',
                'Type' : 1
                }

                form = RegisterForm(data=data)
                #form should not be valid since there is missing data
                self.assertFalse(form.validate())
                error_dict = form.errors
                #check if error message for missing email is displayed
                self.assertIn('Please enter a name', error_dict.get('Name', []))


    #need to add app context 
    #testing that an exisiting user can log in 
    def test_login(self):
        #using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : 'michael.scott@gmail.com',
                    'Password' : '12345678',
                    'Type' : 1
                }

                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)




 
     #logging in a user with missing fields
     #an error message should be displayed to the user 
    def test_invalid_login(self):
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : ' ',
                    'Password' : '12345678'
                }

                form = LoginForm(data=data)
                self.assertFalse(form.validate())
                error_dict = form.errors
                self.assertIn('Please enter your email', error_dict.get('Email', []))

    

    # # #testing that if a user books an event, it shows up on their my bookings page
    # def test_bookedActivityShowsUp(self):
    #     self.user2 = UserLogin(email = 'jim.halpert@gmail.com', password = '12345678', userType = 1)
    #     db.session.add(self.user2)
    #     db.session.commit()

    #     with self.app:
    #         self.app.post('/login', data=dict(
    #             email = self.user2.email,
    #             password = self.user2.password,
    #             userType = self.user2.userType
    #         ))

    #         #create a new activity 
    #         self.activity1 = Activity(activityType = 'Test Activity')
    #         db.session.add(self.activity1)
    #         db.session.commit()

    #         #make a calendar event for the activity 

    #         #book the activity 
    #         self.app.post(f'/calendar/{self.activity1.id}/makeBooking')

    #         #check if activity shows up on the user's my bookings page 
    #         response = self.app.get('/myBookings')
    #         self.assertIn(self.activity1.activityType.encode(), response.data)

    #testing that is a user cancels their booking, it is removed from their my bookings page 
