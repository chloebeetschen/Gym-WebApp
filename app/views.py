from flask import Flask, render_template, flash, url_for, redirect
from app import app, db, models, admin
from .models import UserLogin
from .forms import *
from flask_login import current_user, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_admin.contrib.sqla import ModelView

bcrypt = Bcrypt(app)

admin.add_view(ModelView(UserLogin, db.session))

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "Login"

@app.before_first_request
def create_tables():
    db.create_all()

@loginManager.user_loader
def loadUser(userId):
    return models.UserLogin.query.get(int(userId))

@app.route('/')
@login_required
def index():
    #check the user type
    if current_user.userType == 3:
        admin.add_view(ModelView(UserLogin, db.session))
    if currentUser.userType == 2:
        return '<h1>This is working.</h1>'
    if currentUser.userType == 1:
        return '<h1>This is working.</h1>' 


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

    return render_template('login.html',
                            form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
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
        Name = form.Name.data
        dob = form.DateOfBirth.data
        Address = form.Address.data
        Email = form.Email.data
        hashedPassword = bcrypt.generate_password_hash(form.Password.data)

        # Create new user and details
        newUser = models.UserLogin(email=Email, password=hashedPassword, userType =1) #users that register are automatically set to 1
        newUserDetails = models.UserDetails(name=Name, dateOfBirth=dob, address=Address, loginDetails=newUser.id)

        # Add to the database
        db.session.add(newUser)
        db.session.add(newUserDetails)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html',
                            form = form)

@app.route('/home', methods=['GET', 'POST'])
@login_required # You have to be logged in to see the homepage
def home():
    return render_template('home.html', title='home')

