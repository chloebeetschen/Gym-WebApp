from flask import Flask, render_template, flash, url_for, redirect
from app import app, db, models
from .forms import *
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

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
        usedEmail = models.UserLogin.query.filer_by(email=form.email.data).first()
        if usedEmail:
            flash("Looks like this email is already in use. Please log in.")
            return redirect(url_for('login'))

        # Get data from the form
        Name = form.name.data
        dob = form .dateOfBirth.data
        Address = form.address.data
        Email = form.email.data
        hashedPassword = bcrypt.generate_password_hash(form.password.data)

        # Create new user and details
        newUser = models.UserLogin(email=Email, password=hashedPassword)
        newUserDetails = models.UserDetails(name=Name, date=dob, address=Address, parentId=newUser.id)

        # Add to the database
        db.session.add_all([newUser, newUserDetails])
        db.session.commit()

    return render_template('register.html',
                            form = form)
