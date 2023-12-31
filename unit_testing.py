# Used chat gpt to learn how to use unit test in python 

import unittest
import logging
from flask import Flask, current_app, url_for, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models 
from app.models import *
from app.views import *
from app.forms import *
from flask.testing import FlaskClient 
from test_config import *


class TestCase(unittest.TestCase):

    # This is setting up a test database 
    def setUp(self):
        app.config.from_object('test_config')
        self.app = app.test_client()  
        db.create_all() 
        # Setting up the log file to record test outputs 
        self.logger = logging.getLogger('my_logger')
        handler = logging.FileHandler('test.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    # This deletes the test database once testing is complete 
    def tearDown(self):
        db.session.remove()
        db.drop_all()
       # Closing the log file 
        for handler in self.logger.handlers:
            handler.close()
        self.logger.removeHandler(handler)



    # Testing that different pages load 
    def test_meetTheTeam(self):
        response = self.app.get(('/meetTheTeam'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("meet the team page: P")
        except AssertionError:
            self.logger.warning("meet the team page: F")
            raise
    
    def test_termsAndCond(self):
        response = self.app.get(('/termsAndConditions'), follow_redirects=True)
        try:
            self.assertEqual(response.status_code, 200)
            self.logger.info("terms and conditions page: P")
        except AssertionError:
            self.logger.warning("terms and conditions page: F")
            raise

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


    # Registering a user and testing if this updates in the database
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
                # Testing if the database is updated when a user registers, for login db and details db
                user = models.UserDetails.query.filter_by(name= 'Michael Scott').first()
                user = models.UserLogin.query.filter_by(email= 'michael.scott@gmail.com').first()
                try:
                    self.assertIsNotNone(user)
                    self.logger.info('registering new user: P')
                except AssertionError:
                    self.logger.warning('registering new user: F')
                    raise


    # Registering the same user twice - should not work as their email already exists in the db
    def test_registerSame(self):
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        # Registering a new user first
        with app.test_request_context():
            with app.app_context():
                data = {
                    'Name' : 'Hope Brooke',
                    'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                    'Email' : 'hope.b@gmail.com',
                    'Password' : 'MichaelScott1',
                    'ReenterPassword' : 'MichaelScott1',
                    'Type' : 1
                    }
                form = RegisterForm(data=data)
                self.assertTrue(form.validate())
                if not form.validate():
                    print(form.errors)
                response = self.app.post('/register', data=data)

                # Testing if the database is updated when a user registers, for login db
                user = models.UserDetails.query.filter_by(name= 'Hope Brooke').first()

                # Now try to re-register the same user
                response = self.app.get(('/register'), follow_redirects = True)
                self.assertEqual(response.status_code, 200)

                # Registering the same user again
                with app.test_request_context():
                    with app.app_context():
                        data = {
                        'Name' : 'Hope Brooke',
                        'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                        'Email' : 'hope.b@gmail.com',
                        'Password' : 'MichaelScott1',
                        'ReenterPassword' : 'MichaelScott1',
                        'Type' : 1
                        }
                        form = RegisterForm(data=data)
                        response = self.app.post('/register', data=data)

                        # Counting the number of users registered with name Hope Brooke
                        user_count = models.UserDetails.query.filter_by(name= 'Hope Brooke').count()
                        try:
                            # Should only be 1 user 
                            self.assertEqual(user_count, 1)
                            self.logger.info('Unable to register the same user twice: P')
                        except AssertionError:
                            self.logger.warning('Unable to register the same user twice: F')
                        

    # Registering another user and testing if this updates in the database
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
                try:
                    self.assertIsNotNone(user)
                    self.logger.info('registering new user number 2: P')
                except AssertionError:
                    self.logger.warning('registering new user number 2: F')
                    raise


    # Testing to see if we can register a user with missing details - should not be able to
    # Missing email field 
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
                # Form should not be valid since there is missing data
                self.assertFalse(form.validate())
                error_dict = form.errors
                # Check if error message for missing email is displayed
                self.assertIn('This field is required.', error_dict.get('Email', []))
                # Check if the user is created in the database - they should not be 
                user = models.UserDetails.query.filter_by(name= 'Pam Halpert').first()
                try:
                    self.assertIsNone(user)
                    self.logger.info('User not registered: P')
                except AssertionError:
                    self.logger.warning('User not registered: F')
                    raise


    # Testing to see if we can register a user with missing details - should not be able to
    # Missing Name field 
    def test_registerMissing2(self):
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
                # Form should not be valid since there is missing data
                self.assertFalse(form.validate())
                error_dict = form.errors
                # Check if error message for missing email is displayed
                self.assertIn('This field is required.', error_dict.get('Name', []))
                # Check if the user is created in the database - they should not be 
                user = models.UserLogin.query.filter_by(email= 'Pam.halpert@gmail.com').first()
                try:
                    self.assertIsNone(user)
                    self.logger.info('User not registered 2: P')
                except AssertionError:
                    self.logger.warning('User not registered 2: F')
                    raise
                

    # Testing that an exisiting user can log in 
    def test_login(self):
        # Using the login details of an already registered user
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
                try:
                    self.assertEqual(response.status_code, 200)
                    self.logger.info('Existing user logged in: P')
                except AssertionError:
                    self.logger.warning('Existing user logged in: F')
                    raise
                

    # Logging in a user with missing fields
    # An error message should be displayed to the user 
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
                try:
                    self.assertIn('This field is required.', error_dict.get('Email', []))
                    self.logger.info('User could not login with missing field: P')
                except AssertionError:
                    self.logger.warning('User could not login with missing field: F')
                    raise


    # Check privileges - a customer of type1 that is logged in should not be able to access pages for userType 3 accounts
    # Testing that an exisiting user can log in 
    def test_user_privilege1(self):
        # Using the login details of an already registered user
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
                # The user tries to access the manager page analysis
                response = self.app.get('/editEvent')
                # 404 = page does not exist becuase no event id has been passed in 
                try:
                    self.assertEqual(response.status_code, 404)
                    self.logger.info('Customer couldnt access edit event page: P')
                except AssertionError:
                    self.logger.warning('Customer couldnt access edit event page: F')
                    raise
                
    
    # The same as previous test but for other manager only pages 
    def test_user_privilege2(self):
        # Using the login details of an already registered user
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
                # The user tries to access the manager page analysis
                response = self.app.get('/manageUsers')
                # 302 = the user is redirected 
                try:
                    self.assertEqual(response.status_code, 302)
                    self.logger.info('Customer couldnt access manage Users page: P')
                except AssertionError:
                    self.logger.warning('Customer couldnt access manage Users page: F')
                    raise


    # The same as previous test but for other manager only pages 
    def test_user_privilege3(self):
        # Using the login details of an already registered user
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
        
                # The user tries to access the manager page analysis
                response = self.app.get('/editUser')
                # 404 = page does not exist because no userID passed to html
                try:
                    self.assertEqual(response.status_code, 404)
                    self.logger.info('Customer couldnt access edit user page: P')
                except AssertionError:
                    self.logger.warning('Customer couldnt access edit user page: F')
                    raise


    # The same as previous test but for other manager only pages 
    def test_user_privilege4(self):
        # Using the login details of an already registered user
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
        
                # The user tries to access the manager page analysis
                response = self.app.get('/analysis')
                # 302 = the user is redirected 
                try:
                    self.assertEqual(response.status_code, 302)
                    self.logger.info('Customer couldnt access analysis page: P')
                except AssertionError:
                    self.logger.warning('Customer couldnt access analysis page: F')


    # The same as previous test but for other manager only pages 
    def test_user_privilege5(self):
        # Using the login details of an already registered user
        response = self.app.get(('/login'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():
                data = {
                    'Email' : 'aaditi@gmail.com',
                    'Password' : 'MichaelScott1'
                }
                form = LoginForm(data=data)
                self.assertTrue(form.validate())
                response = self.app.post('/login', data=form.data, follow_redirects = True)
                self.assertEqual(response.status_code, 200)
        
                # The user tries to access the manager page analysis
                response = self.app.get('/editActivity')
                # 302 = the user is redirected 
                try:
                    self.assertEqual(response.status_code, 302)
                    self.logger.info('Customer couldnt access edit Activity page: P')
                except AssertionError:
                    self.logger.warning('Customer couldnt access edit Activity page: F')
    

    # Change just the user's name
    def test_userDetail_update(self):
        # First register a user 
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():
                data = {
                    'Name' : 'Harry Potter',
                    'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                    'Email' : 'harry@gmail.com',
                    'Password' : 'HarryPotter1',
                    'ReenterPassword' : 'HarryPotter1',
                    'Type' : 1
                    }
                form = RegisterForm(data=data)
                self.assertTrue(form.validate())
                if not form.validate():
                    print(form.errors)
                response = self.app.post('/register', data=data)
                
                # Then login as user
                response = self.app.get(('/login'), follow_redirects = True)
                self.assertEqual(response.status_code, 200)
                with app.test_request_context():
                    with app.app_context():
                        data1 = {
                            'Email' : 'harry@gmail.com',
                            'Password' : 'HarryPotter1',
                        }
                        form = LoginForm(data=data1)
                        self.assertTrue(form.validate())
                        response = self.app.post('/login', data=form.data, follow_redirects=True)
                        self.assertEqual(response.status_code, 200)
                        
                        # Then change name
                        response = self.app.get(('/settings'), follow_redirects = True)
                        self.assertEqual(response.status_code, 200)
                        with app.test_request_context():
                            with app.app_context():
                                data2 = {
                                    'Name' : 'Dumbledore',
                                    'Password' : 'HarryPotter1'
                                }
                                form = SettingsForm(data=data2)
                                self.assertTrue(form.validate())
                                response = self.app.post('/settings', data=form.data, follow_redirects=True)
                                self.assertEqual(response.status_code, 200)

                                # Get the account of the user
                                user = models.UserLogin.query.filter_by(email='harry@gmail.com').first()
                                # Check that name has changed
                                usersName = models.UserDetails.query.filter_by(id=user.id).first()
                                try:
                                    self.assertEqual(usersName.name, 'Dumbledore')
                                    self.logger.info('User changing name: P')
                                except AssertionError:
                                    self.logger.warning('User changing name: F')
                                    raise
                                

    # If a user updates their password 
    # The changes should be reflected in the userDetails database
    def test_userDetail_updatePassword(self):
        # First register a user 
        response = self.app.get(('/register'), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            with app.app_context():
                data = {
                    'Name' : 'Hermione Granger',
                    'DateOfBirth' : datetime.strptime('2002-03-15', '%Y-%m-%d').date(),
                    'Email' : 'hermione@gmail.com',
                    'Password' : 'Hermione1',
                    'ReenterPassword' : 'Hermione1',
                    'Type' : 1
                    }
                form = RegisterForm(data=data)
                self.assertTrue(form.validate())
                if not form.validate():
                    print(form.errors)
                response = self.app.post('/register', data=data)
                
                # Then login as user
                response = self.app.get(('/login'), follow_redirects = True)
                self.assertEqual(response.status_code, 200)
                with app.test_request_context():
                    with app.app_context():
                        data1 = {
                            'Email' : 'hermione@gmail.com',
                            'Password' : 'Hermione1',
                        }
                        form = LoginForm(data=data1)
                        self.assertTrue(form.validate())
                        response = self.app.post('/login', data=form.data, follow_redirects=True)
                        self.assertEqual(response.status_code, 200)
                        
                        # Then change password
                        response = self.app.get(('/settings'), follow_redirects = True)
                        self.assertEqual(response.status_code, 200)
                        with app.test_request_context():
                            with app.app_context():
                                data2 = {
                                    'Password' : 'Hermione1',
                                    'NewPassword' : 'Hermione2',
                                    'NewPasswordx2' : 'Hermione2'

                                }
                                form = SettingsForm(data=data2)
                                self.assertTrue(form.validate())
                                response = self.app.post('/settings', data=form.data, follow_redirects=True)
                                self.assertEqual(response.status_code, 200)

                                # Then logout
                                response = self.app.get(('/logout'), follow_redirects = True)
                                # Login again
                                response = self.app.get(('/login'), follow_redirects = True)
                                self.assertEqual(response.status_code, 200)
                                with app.test_request_context():
                                    with app.app_context():
                                        data3 = {
                                            'Email' : 'hermione@gmail.com',
                                            'Password' : 'Hermione2',
                                        }
                                        form = LoginForm(data=data3)
                                        self.assertTrue(form.validate())
                                        response = self.app.post('/login', data=form.data, follow_redirects=True)
                                        try:
                                            self.assertEqual(response.status_code, 200)
                                            self.logger.info('Password changed: P')
                                        except AssertionError:
                                            self.logger.warning('Password changed: F')
                                            raise

