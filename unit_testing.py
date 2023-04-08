#pair programming - Aaditi and Hope 
#used chat gpt to learn how to use unit test in python 

#test 11 and test 8 don't run... idk why !!!!!!
#need to run the tests after password regex stuff is merged, the test should still pass 

import unittest
import logging
from flask import Flask, current_app, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models 
from app.models import *
from app.views import *
from app.forms import *
from flask.testing import FlaskClient 
from test_config import *


class TestCase(unittest.TestCase):

    #this is setting up a test database 
    def setUp(self):
        app.config.from_object('test_config')

        self.app = app.test_client()  
        db.create_all() 

        #setting up the log file to record test outputs 
        self.logger = logging.getLogger('my_logger')
        handler = logging.FileHandler('test.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

       
    #this deletes the test database once testing is complete 
    def tearDown(self):
      db.session.remove()
      db.drop_all()

      #closing the log file 
      for handler in self.logger.handlers:
        handler.close()
        self.logger.removeHandler(handler)


    #testing that different pages load 
    def test_navBarAll_register(self):
        response = self.app.get(('/register'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("register page: P")
        except AssertionError:
            self.logger.warning("register page: F")
            raise

    def test_navBarAll_home(self):
        response = self.app.get(('/home'), follow_redirects = True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("home page: P")
        except AssertionError:
            self.logger.warning("home page: F")
            raise

    def test_navBarAll_login(self):
        response = self.app.get(('/login'), follow_redirects = True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("login page: P")
        except AssertionError:
            self.logger.warning("login page: F")
            raise

    def test_navBarType1_myBookings(self):
        response = self.app.get(('/myBookings'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("myBookings page: P")
        except AssertionError:
            self.logger.warning("myBookings page: F")
            raise
    
    def test_navBarType1_calendar(self):
        response = self.app.get(('/calendar'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("calendar page: P")
        except AssertionError:
            self.logger.warning("calendar page: F")
            raise


    def test_navBarType1_settings(self):
        response = self.app.get(('/settings'), follow_redirects = True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("settings page: P")
        except AssertionError:
            self.logger.warning("settings page: F")
            raise

    def test_navBarType1_basket(self):
        response = self.app.get(('/basket'), follow_redirects = True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("basket page: P")
        except AssertionError:
            self.logger.warning("basket page: F")
            raise
    
    def test_navBarType1_memberships(self):
        response = self.app.get(('/memberships'), follow_redirects = True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("memberships page: P")
        except AssertionError:
            self.logger.warning("memberships page: F")
            raise   

    # NOT RUNNING
    def test_navBarType2_manageUsers(self):
        response = self.app.get(('/manageUsers'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("manageUsers page: P")
        except AssertionError:
            self.logger.warning("managerUsers page: F")
            raise  

    def test_navBarType3_addEvent(self):
        response = self.app.get(('/addEvent'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("addEvent page: P")
        except AssertionError:
            self.logger.warning("addEvent page: F")
            raise  

    def test_navBarType3_addActivity(self):
        response = self.app.get(('/addActivity'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("addActivity page: P")
        except AssertionError:
            self.logger.warning("addActivity page: F")
            raise  
    
    def test_navBarType3_analysis(self):
        response = self.app.get(('/analysis'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("analysis page: P")
        except AssertionError:
            self.logger.warning("analysis page: F")
            raise  


    #registering a user and testing if this updates in the database
    def test_register(self):
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

        with app.test_request_context():
            with app.app_context():
                data = {
                    'Name' : 'Michael Scott',
                    'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                    'Email' : 'michael.scott@gmail.com',
                    'Password' : 'MichaelScott1',
                    'ReenterPassword' : 'MichaelScott1',
                    'Type' : 1
                    }

                form = RegisterForm(data=data)
                self.assertTrue(form.validate())
                if not form.validate():
                    print(form.errors)

                response = self.app.post('/register', data=data)
                
                #testing if the database is updated when a user registers, for login db and details db
                user = models.UserDetails.query.filter_by(name= 'Michael Scott').first()
                user = models.UserLogin.query.filter_by(email= 'michael.scott@gmail.com').first()
                self.assertIsNotNone(user)
                print(10)

    #registering a user and testing if this updates in the database
    def test_register2(self):
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)

        with app.test_request_context():
            with app.app_context():
                data = {
                    'Name' : 'Aaditi Agrawal',
                    'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                    'Email' : 'aaditi@gmail.com',
                    'Password' : 'MichaelScott1',
                    'ReenterPassword' : 'MichaelScott1',
                    'Type' : 1
                    }

                form = RegisterForm(data=data)
                self.assertTrue(form.validate())
                if not form.validate():
                    print(form.errors)

                response = self.app.post('/register', data=data)
                
                user = models.UserDetails.query.filter_by(name= 'Aaditi Agrawal').first()
                user = models.UserLogin.query.filter_by(email= 'aaditi@gmail.com').first()
                self.assertIsNotNone(user)
                print(19)


    # NOT RUNNING 
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
                'Email' : ' ',
                'Password' : 'MichaelScott1',
                'ReenterPassword' : 'MichaelScott1',
                'Type' : 1
                }

                form = RegisterForm(data=data)
                #form should not be valid since there is missing data
                self.assertFalse(form.validate())
                error_dict = form.errors
                #check if error message for missing email is displayed
                self.assertIn('This field is required.', error_dict.get('Email', []))
                print(11)

    
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
                'Email' : 'Pam.halpert@gmail.com',
                'Password' : 'MichaelScott1',
                'ReenterPassword' : 'MichaelScott1',
                'Type' : 1
                }

                form = RegisterForm(data=data)
                #form should not be valid since there is missing data
                self.assertFalse(form.validate())
                error_dict = form.errors
                #check if error message for missing email is displayed
                self.assertIn('This field is required.', error_dict.get('Name', []))
                print(12)


    #testing that an exisiting user can log in 
    def test_login(self):
        #using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : 'michael.scott@gmail.com',
                    'Password' : 'MichaelScott1',
                }

                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)
                print(13)


    #logging in a user with missing fields
    #an error message should be displayed to the user 
    def test_invalid_login(self):
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : ' ',
                    'Password' : 'MichaelScott1',
                }

                form = LoginForm(data=data)
                self.assertFalse(form.validate())
                error_dict = form.errors
                self.assertIn('This field is required.', error_dict.get('Email', []))
                print(14)


    #check privileges - a customer of type1 that is logged in should not be able to access pages for userType 3 accounts
    #testing that an exisiting user can log in 
    def test_user_privilege1(self):
        #using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : 'aaditi@gmail.com',
                    'Password' : 'MichaelScott1',
                }

                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)
        
                #the user tries to access the manager page analysis
                response = self.app.get('/editEvent')
                #404 = page does not exist becuase no event id has been passed in 
                self.assertEqual(response.status_code, 404)
                print(15)
    
    #the same as previous test but for other manager only pages 
    def test_user_privilege2(self):
        #using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : 'aaditi@gmail.com',
                    'Password' : 'MichaelScott1',
                }

                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)
        
                #the user tries to access the manager page analysis
                response = self.app.get('/manageUsers')
                #302 = the user is redirected 
                self.assertEqual(response.status_code, 302)
                print(20)


    #the same as previous test but for other manager only pages 
    def test_user_privilege3(self):
        #using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : 'aaditi@gmail.com',
                    'Password' : 'MichaelScott1',
                }

                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)
        
                #the user tries to access the manager page analysis
                response = self.app.get('/editUser')
                #404 = page does not exist because no userID passed to html
                self.assertEqual(response.status_code, 404)
                print(21)


    #the same as previous test but for other manager only pages 
    def test_user_privilege4(self):
        #using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : 'aaditi@gmail.com',
                    'Password' : 'MichaelScott1',
                }

                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)
        
                #the user tries to access the manager page analysis
                response = self.app.get('/analysis')
                #302 = the user is redirected 
                self.assertEqual(response.status_code, 302)
                print(22)

    #the same as previous test but for other manager only pages 
    def test_user_privilege5(self):
        #using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():

                data = {
                    'Email' : 'aaditi@gmail.com',
                    'Password' : 'MichaelScott1',
                }

                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)
        
                #the user tries to access the manager page analysis
                response = self.app.get('/editActivity')
                #302 = the user is redirected 
                self.assertEqual(response.status_code, 302)
                print(23)



