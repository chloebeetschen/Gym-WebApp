from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField, DateTimeLocalField
from wtforms import StringField, BooleanField, IntegerField, FloatField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from luhn import *
from datetime import *
# from .models import Activity



# Function to check that card number is a Luhn number
def validateLuhn(form, field):
     if verify(str(field.data)) == False:
         raise ValidationError('Card Number is not valid')


# Function to check that a date is in the future
def validateFutureDate(form, field):
    if field.data < datetime.now():
        raise ValidationError('You must enter a date in the future')


# Function to check that registree is old enough to register
def validateAge(form, field):
    oldEnough = datetime.now().date()-timedelta(days=16*365)
    if field.data > oldEnough:
        raise ValidationError("You are not old enough to register")


# For the manager to add a new activity e.g. swimming
# Can be used for editing and creating activities
class ActivityForm(FlaskForm):
    aType       = StringField('Type', validators=[DataRequired(message="Please enter an activity type")])


# Form to add an activity to the calendar
# Can be used for editing and adding calendar events
class EventForm(FlaskForm):

    aDateTime    = DateTimeLocalField('Date & Time of activity', format='%Y-%m-%dT%H:%M', validators=[DataRequired(message="Please enter a Date & Time"), validateFutureDate], render_kw={"placeholder": "Date of activity"})
    aDuration    = IntegerField('Duration of activity', validators=[DataRequired(message="Please enter a duration"), NumberRange(min=0, message="Please enter a positive duration")],
                             render_kw={"placeholder": "Duration of activity"})
    aStaffName   = StringField("Staff Name", validators=[DataRequired(message="Please enter an staff name")], render_kw={"placeholder": "Staff Member"}) 
    aLocation    = StringField("Location", validators=[DataRequired(message="Please enter a location")], render_kw={"placeholder": "Location"}) 
    aPrice       = FloatField("Price", validators=[DataRequired(message="Please enter a price"), NumberRange(min=0.0, message="Please enter a positive price")], render_kw={"placeholder": "Price of activity"}) 
    aCapacity    = IntegerField('Capacity of activity', validators=[DataRequired(message="Please enter a capacity"), NumberRange(min=0, message="Please enter a postive capacity")],
                               render_kw={"placeholder": "Capacity of activity"})

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
    DateOfBirth = DateField('Date of birth', validators=[DataRequired(message="Please enter your date of birth"), validateAge], render_kw={"placeholder": "Date of Birth"})
    Email       = EmailField('Email', validators=[DataRequired(message="Please enter an email")], render_kw={"placeholder": "Email"})
    Password    = PasswordField('Password', validators=[DataRequired(message="Please enter a password"), Length(min=8, message="Password must be 8 characters or more")], render_kw={"placeholder": "Password"})
    ReenterPassword = PasswordField('Reenter Password', validators=[DataRequired(message="Please reenter your password"), 
                                                                    EqualTo('Password', message="Passwords must match")],
                                                                    render_kw={"placeholder": "Reenter Password"})
    Type        = IntegerField('Type', validators=[DataRequired(message="Please enter a type"), NumberRange(min=1, max=3)], render_kw={"placeholder": "Type"})


class LoginForm(FlaskForm):
    Email       = EmailField('email', validators=[DataRequired(message="Please enter a your email")], render_kw={"placeholder": "Email"})
    Password    = PasswordField('password', validators=[DataRequired(message="Please enter your password")], render_kw={"placeholder": "Password"})


class SettingsForm(FlaskForm):
    Name          = StringField('Name', validators=[DataRequired(message="Please enter your name")], render_kw={"placeholder": "Name"})
    Password      = PasswordField('Old Password', validators=[DataRequired(message="Please enter your old password")], render_kw={"placeholder": "Password"})
    NewPassword   = PasswordField('New Password', validators=[DataRequired(message="Please enter a new password"), Length(min=8, message="Password must be 8 characters or more")], render_kw={"placeholder": "New Password"})
    NewPasswordx2 = PasswordField('Reenter New Password', validators=[DataRequired(message="Please re-enter your new password"), EqualTo('NewPassword', message="Passwords must match")], render_kw={"placeholder": "Reenter New Password"})

class ManagerForm(FlaskForm):
    Name          = StringField('Name', render_kw={"placeholder": "Name"})
    Email         = EmailField('email', validators=[DataRequired(message="Please enter a your email")], render_kw={"placeholder": "Email"})
    NewPassword   = PasswordField('New Password', validators=[DataRequired(message="Please enter a new password"), Length(min=8, message="Passwords must be 8 characters or more")], render_kw={"placeholder": "New Password"})
    NewPasswordx2 = PasswordField('Reenter New Password', validators=[DataRequired(message="Please reenter the new password"), EqualTo('NewPassword', message="Passwords must match")], render_kw={"placeholder": "Reenter New Password"})
    Type        = IntegerField('Type', validators=[DataRequired(message="Please enter a type"), NumberRange(min=1, max=3, message="Type must be 1, 2 or 3")], render_kw={"placeholder": "Type"})

