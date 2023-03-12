#pair programming - Aaditi and Hope 
#used chat gpt to learn how to use unit test in python  


import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models 
from app.models import *


class TestCase(unittest.TestCase):

    #this is setting up a test database 
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

        #populating the database with test data 
        self.user1 = UserLogin(email = 'michael.scott@gmail.com', password = '12345678', userType = '1')
        db.session.add(self.user1)
        db.session.commit()

        pass

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


    #for user type 1  
    def test_navBarType1_myBookings(self):
        response = self.app.get(('/myBookings'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_navBarType1_calendar(self):
        response = self.app.get(('/calendar'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    #TO DO :
    #basket page 
    #payment page 
    #detail page


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

    #TO DO :
    #manage users page 
    #def test_navBarType2_manageUsers(self):
        #response = self.app.get(('/manageUsers'), follow_redirects=True)
        #self.assertEqual(response.status_code, 200)  



    #testing the form fields for log in 
    def test_login(self):
        response = self.app.post('/login', data=dict(
            email = self.user1.email,
            password = self.user1.password,
            userType = self.user1.userType
        ), follow_redirects = True)
        self.assertEqual(response.status_code, 200)


    def test_invalid_login(self):
        response = self.app.post('/login', data=dict(
            email = 'invalid',
            password = 'invalid',
            userType = 'invalid'
        ), follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        