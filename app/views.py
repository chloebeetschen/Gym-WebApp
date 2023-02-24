from flask import Flask, render_template, flash, url_for, redirect
from app import app, db, models
from .forms import *
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return '<h1>This is working.</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                            form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check that the email hasn't been used already.
        usedEmail = models.UserLogin.query.filter_by(email=form.Email.data).first()
        print(1)
        if usedEmail:
            flash("Looks like this email is already in use. Please log in.")
            return redirect(url_for('login'))

        # Get data from the form
        Name = form.Name.data
        dob = form.DateOfBirth.data
        Address = form.Address.data
        Email = form.Email.data
        hashedPassword = bcrypt.generate_password_hash(form.Password.data)

        # Create new user and details
        newUser = models.UserLogin(email=Email, password=hashedPassword)
        newUserDetails = models.UserDetails(name=Name, dateOfBirth=dob, address=Address, loginDetails=newUser.id)
        print(2)

        # Add to the database
        db.session.add(newUser)
        db.session.add(newUserDetails)
        db.session.commit()
        print(3)

    return render_template('register.html',
                            form = form)
