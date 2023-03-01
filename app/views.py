from flask import Flask, render_template, flash, url_for, redirect
from app import app, db, models, admin
from .models import UserLogin, PaymentCard
from .forms import *
from flask_admin.contrib.sqla import ModelView

from flask_login import current_user, login_user, LoginManager, login_required
from flask_login import logout_user, current_user

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Register tables with flask admin
admin.add_view(ModelView(UserLogin, db.session))
admin.add_view(ModelView(PaymentCard, db.session))

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
    # check the user type
    # If admin, show them the admin page
    if current_user.userType == 3:
        admin.add_view(ModelView(UserLogin, db.session))
    elif current_user.userType == 2 or current_user.userType == 1:
        return redirect(url_for('home'))


#Payment Form page
@app.route('/paymentForm', methods=['GET', 'POST'])
def paymentForm():
    form = PaymentForm()
    
    # Add data to database on submit:
    if form.validate_on_submit():
        # Create Payment Card field with entered details
        newCard = models.PaymentCard(cardName=form.cName.data,
                                     cardNum=form.cNum.data,
                                     cardExpDate=form.cExpDate.data,
                                     cardCVV=form.cCVV.data)

        # Add new card entry to database and commit
        db.session.add(newCard)
        db.session.commit()

        flash('Payment details registered')
    return render_template('paymentForm.html', title='Payment Form', form=form)


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

    return render_template('login.html', form=form)


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
        Name    = form.Name.data
        dob     = form.DateOfBirth.data
        Address = form.Address.data
        Email   = form.Email.data
        hashedPassword = bcrypt.generate_password_hash(form.Password.data)

        # Create new user and details
        # users that register are automatically set to 1
        newUser = models.UserLogin(email=Email,
                                   password=hashedPassword,
                                   userType=1)
        newUserDetails = models.UserDetails(name=Name,
                                            dateOfBirth=dob,
                                            address=Address,
                                            loginDetails=newUser.id)

        # Add to the database
        db.session.add(newUser)
        db.session.add(newUserDetails)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='home')
