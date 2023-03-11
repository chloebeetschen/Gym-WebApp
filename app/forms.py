from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField
from wtforms import StringField, BooleanField, IntegerField, FloatField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from luhn import *
from datetime import *
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
    oldEnough = datetime.now().date()-timedelta(days=16*365)
    if field.data > oldEnough:
        raise ValidationError("You are not old enough to register")


# For the manager to add a new activity e.g. swimming
# Can be used for editing and creating activities
class ActivityForm(FlaskForm):
    aType       = StringField('aType', validators=[DataRequired()])


# Form to add an activity to the calendar
# Can be used for editing and adding calendar events
class EventForm(FlaskForm):
    aDateTime    = DateField('Date of activity', validators=[DataRequired()], render_kw={"placeholder": "Date of activity"})
    aDuration    = IntegerField('Duration of activity', validators=[DataRequired()],
                                render_kw={"placeholder": "Duration of activity"})
    aStaffName   = StringField("Staff Name", validators=[DataRequired()], render_kw={"placeholder": "Staff Member"}) 
    aLocation    = StringField("Location", validators=[DataRequired()], render_kw={"placeholder": "Location"}) 
    aPrice       = FloatField("Price", validators=[DataRequired()], render_kw={"placeholder": "Price of activity"}) 
    aCapacity    = IntegerField('Capacity of activity', validators=[DataRequired()],
                               render_kw={"placeholder": "Capacity of activity"})
    # The activity id slot will be added in the html and passed in the route




# Form to create account:
class PaymentForm(FlaskForm):
    cName = StringField('Name', validators=[DataRequired(message="Please enter a name")], render_kw={"placeholder": "Cardholder Name"})
    cNum  = IntegerField('Card number',
                     validators=[DataRequired(message='Please enter a card number'), 
                     NumberRange(min=1000000000000000, max=9999999999999999, message='Card number needs to be 16 digits'),
                     validateLuhn], render_kw={"placeholder": "Card Number"})

    cExpDate = DateField('Expiry',
                      validators=[DataRequired(message='Please enter an expiry date'),
                      validateFutureDate], render_kw={"placeholder": "Expiry Date"})
                      
    cCVV = IntegerField('CVV', 
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
