from flask_wtf import FlaskForm
import datetime
from wtforms import PasswordField, EmailField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField
from wtforms import StringField, BooleanField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from luhn import *
# from .models import Activity


timeChoices = [(700,'07:00'),  (730,'07:30'),  (800,'08:00'),  (830,'08:30'),
               (900,'09:00'),  (900,'09:30'),  (1000,'10:00'), (1030,'10:30'),
               (1100,'11:00'), (1130,'11:30'), (1200,'12:00'), (1230,'12:30'),
               (1300,'13:00'), (1330,'13:30'), (1400,'14:00'), (1430,'14:30'),
               (1500,'15:00'), (1530,'15:30'), (1600,'16:00'), (1630,'16:30'),
               (1700,'17:00'), (1730,'17:30'), (1800,'18:00'), (1830,'18:30'),
               (1900,'19:00'), (1930,'19:30'), (2000,'20:00'), (2030,'20:30'),
               (2100,'21:00'), (2130,'21:30')]


# function to check that card number is a Luhn number
def validateLuhn(form, field):
     if verify(str(field.data)) == False:
         raise ValidationError('Card Number is not valid')


# Function to check that a date is in the future
def validateFutureDate(form, field):
    if field.data < datetime.date.today():
        raise ValidationError('You must enter a date in the future')


# Function to check that registree is old enough to register
def validateAge(form, field):
    oldEnough = datetime.date.today() - datetime.timedelta(days=16*365)
    if field.data > oldEnough:
        raise ValidationError("You are not old enough to register")


# Form for the manager to add a new activity e.g. swimming
class addActivityForm(FlaskForm):
    aType       = StringField('aType', validators=[DataRequired(message="Please enter a type")], render_kw={"placeholder": "Type"})
    aPrice      = DecimalField('aPrice', places=2, validators=[DataRequired(message="Please enter a price"), NumberRange(min=0, max=10000)], render_kw={"placeholder": "Price"})
    aLocation   = StringField('aLocation', validators=[DataRequired(message="Please enter a location")], render_kw={"placeholder": "Location"})
    aCapacity   = IntegerField('aCapacity', validators=[DataRequired(message="Please enter a capacity"), NumberRange(min=0)], render_kw={"placeholder": "Capacity"})
    aStaffName  = StringField('aStaffName', validators=[DataRequired(message="Please enter a staff member name")], render_kw={"placeholder": "Staff Name"})
    addActivity = SubmitField('addActivity')


# Form for the manager to edit an activity e.g. swimming
class editActivityForm(FlaskForm):
    aPrice      = DecimalField('aPrice', places=2, validators=[NumberRange(min=0, max=None, message=("Prices must be above 0"))], render_kw={"placeholder": "Price"})
    aLocation   = StringField('aLocation', render_kw={"placeholder": "Location"})
    aCapacity   = IntegerField('aCapacity', validators=[NumberRange(min=0, message=("Capacities must be above 0"))], render_kw={"placeholder": "Capacity"})
    aStaffName  = StringField('aStaffName', render_kw={"placeholder": "Staff Name"})
    editActivity = SubmitField('editActivity')


# Form for the manager to add a new event  e.g. swimming at a new location/time
class addEventForm(FlaskForm):
    cDate       = DateField('cDate', validators=[DataRequired(message="Please enter a date"), validateFutureDate], render_kw={"placeholder": "Date"})
    #manager can select a time in 30 min increments 
    cTime       = SelectField('cTime', choices=timeChoices, validators=[DataRequired(message="Please enter a time")], render_kw={"placeholder": "Time"})
    cDuration   = SelectField('cDuration', choices = [(30, '30mins'), (60, '60mins')], validators=[DataRequired(message="Please enter a duration")], render_kw={"placeholder": "Duration"})
    #choicesType = [(a.id, a.activityType) for a in Activity.query.all()]
    #cType = SelectField('cType', coerce=int, choices = choicesType, validators=[DataRequired()])
    addEvent    = SubmitField('addEvent')


# Form for the manager to edit an  event  e.g. swimming at a new location/time
class editEventForm(FlaskForm):
    cDate       = DateField('cDate', validators=[validateFutureDate], render_kw={"placeholder": "Date"})
    #manager can select a time in 30 min increments 
    cTime       = SelectField('cTime', choices = timeChoices, render_kw={"placeholder": "Time"})
    cDuration   = SelectField('cDuration', choices = [(30, '30mins'), (60, '60mins')], render_kw={"placeholder": "Duration"})
    editEvent   = SubmitField('editEvent')


# Form to create account:
class PaymentForm(FlaskForm):
    cName       = StringField('Name', validators=[DataRequired(message="Please enter a name")], render_kw={"placeholder": "Cardholder Name"})
    cNum        = IntegerField('Card number',
                        validators=[DataRequired(message='Please enter a card number'), 
                        NumberRange(min=1000000000000000, max=9999999999999999, message='Card number needs to be 16 digits'),
                        validateLuhn], render_kw={"placeholder": "Card Number"})
    cExpDate    = DateField('Expiry',
                         validators=[DataRequired(message='Please enter an expiry date'),
                         validateFutureDate], render_kw={"placeholder": "Expiry Date"})
    cCVV        = IntegerField('CVV', 
                         validators=[DataRequired(message='Please enter the CVV'),
                         NumberRange(min=100, 
                         max=999,
                         message='CVV needs to be 3 digits')], render_kw={"placeholder": "CVV"})


class RegisterForm(FlaskForm):
    Name        = StringField('Name', validators=[DataRequired(message="Please enter a name")], render_kw={"placeholder": "Name"})
    DateOfBirth = DateField('Date of birth', validators=[DataRequired(message="Please enter a name"), validateAge], render_kw={"placeholder": "Date of Birth"})
    Address     = StringField('Address', validators=[DataRequired(message="Please enter an address")], render_kw={"placeholder": "Address"})
    Email       = EmailField('Email', validators=[DataRequired(message="Please enter an email")], render_kw={"placeholder": "Email"})
    Password    = PasswordField('Password', validators=[DataRequired(message="Please enter a password"), Length(min=8)], render_kw={"placeholder": "Password"})
    ReenterPassword = PasswordField('Reenter Password', validators=[DataRequired(message="Please reenter your password"), 
                                                                    EqualTo('Password', message="Passwords must match")],
                                                                    render_kw={"placeholder": "Reenter Password"})
    Type        = IntegerField('Type', validators=[DataRequired(), NumberRange(min=1, max=3)], render_kw={"placeholder": "Type"})


class LoginForm(FlaskForm):
    Email       = EmailField('email', validators=[DataRequired(message="Please enter a your email")], render_kw={"placeholder": "Email"})
    Password    = PasswordField('password', validators=[DataRequired(message="Please enter your password")], render_kw={"placeholder": "Password"})


class SettingsForm(FlaskForm):
    Name        = StringField('Name', render_kw={"placeholder": "Name"})
    Address     = StringField('Address', render_kw={"placeholder": "Address"})
    Password    = PasswordField('Old Password', validators=[DataRequired(message="Please enter your current password")], render_kw={"placeholder": "Password"})
    NewPassword = PasswordField('New Password', validators=[DataRequired(message="Please enter a new password")], render_kw={"placeholder": "New Password"})
    NewPasswordx2 = PasswordField('Reenter New Password', validators=[DataRequired(message="Please reenter your new password"), EqualTo('NewPassword', message="Passwords must match")], render_kw={"placeholder": "Reenter New Password"})