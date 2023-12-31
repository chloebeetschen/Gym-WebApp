from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField, DateTimeLocalField
from wtforms import StringField, BooleanField, IntegerField, FloatField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError, Optional
import re
from datetime import *


# Function to check that a date is in the future
def validateFutureDate(form, field):
    if field.data < datetime.now():
        raise ValidationError('You must enter a date in the future')


# Email format validation
# Email should be of the form xxxxxx@xxx.xxx, with at least one '.' after the @
# Emails should not start or end with a '.'
def validateEmail(form, field):
    regex = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$" )
    if not re.match(regex, field.data):
        raise ValidationError("Not a valid email")


# Function to check that registree is old enough to register but not too old
def validateAge(form, field):
    oldEnough = datetime.now().date()-timedelta(days=16*365)
    youngEnough = datetime.now().date()-timedelta(days=122*365) # The oldest person in the world is 122 - have to be inclusive!
    if field.data > oldEnough:
        raise ValidationError("You are not old enough to register")
    if field.data < youngEnough:
        raise ValidationError("Please enter a valid year")
        

# Ensure password contains capital letter and digit
def passwordPolicy(form, field):
    uppercase = False
    lowercase = False
    digit = False
    for char in field.data:
        if char.isupper():
            uppercase = True
        if char.islower():
            lowercase = True
        if char.isnumeric():
            digit = True
    if (uppercase != True) or (lowercase != True) or (digit != True) :
        raise ValidationError("All passwords must contain an uppercase letter, a lowercase letter and a digit")


# For the manager to add a new activity e.g. swimming
# Can be used for editing and creating activities
class ActivityForm(FlaskForm):
    aType       = StringField('Type', validators=[DataRequired()])


# Search for a user
class SearchForm(FlaskForm):
    search       = StringField('Search')


# Form to add an activity to the calendar
class EventForm(FlaskForm):
    aDateTime    = DateTimeLocalField('Date & Time of activity', format='%Y-%m-%dT%H:%M', validators=[DataRequired(), validateFutureDate], render_kw={"placeholder": "Date of activity"})
    aDuration    = IntegerField('Duration of activity', validators=[DataRequired(), NumberRange(min=0)],
                             render_kw={"placeholder": "Duration of activity"})
    aStaffName   = StringField("Staff Name", validators=[DataRequired()], render_kw={"placeholder": "Staff Member"}) 
    aLocation    = StringField("Location", validators=[DataRequired()], render_kw={"placeholder": "Location"}) 
    aPrice       = FloatField("Price", validators=[NumberRange(min=0.0), DataRequired()], render_kw={"placeholder": "Price of activity"}) 
    aCapacity    = IntegerField('Capacity of activity', validators=[ NumberRange(min=0), DataRequired()],
                               render_kw={"placeholder": "Capacity of activity"})


# Form to edit calendar event
class EditEventForm(FlaskForm):
    aDateTime    = DateTimeLocalField('Date & Time of activity', format='%Y-%m-%dT%H:%M', validators=[Optional(), validateFutureDate], render_kw={"placeholder": "Date of activity"})
    aDuration    = IntegerField('Duration of activity', validators=[Optional(), NumberRange(min=0)],
                             render_kw={"placeholder": "Duration of activity"})
    aStaffName   = StringField("Staff Name", validators=[Optional()], render_kw={"placeholder": "Staff Member"}) 
    aLocation    = StringField("Location", validators=[Optional()], render_kw={"placeholder": "Location"}) 
    aPrice       = FloatField("Price", validators=[NumberRange(min=0.0), Optional()], render_kw={"placeholder": "Price of activity"}) 
    aCapacity    = IntegerField('Capacity of activity', validators=[ NumberRange(min=0), Optional()],
                               render_kw={"placeholder": "Capacity of activity"})


# Form to register a user
class RegisterForm(FlaskForm):
    Name        = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    DateOfBirth = DateField('Date of birth', validators=[DataRequired(), validateAge], render_kw={"placeholder": "Date of Birth"})
    Email       = EmailField('Email', validators=[DataRequired(), validateEmail], render_kw={"placeholder": "Email"})
    Password    = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be 8 characters or more"), passwordPolicy], render_kw={"placeholder": "Password"})
    ReenterPassword = PasswordField('Reenter Password', validators=[DataRequired(), 
                                                                    EqualTo('Password', message="Passwords must match" )],
                                                                    render_kw={"placeholder": "Reenter Password"})


# Form to log in as an existing user
class LoginForm(FlaskForm):
    Email       = EmailField('email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password    = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})


# Form to change a user's details
class SettingsForm(FlaskForm):
    Name          = StringField('Name', render_kw={"placeholder": "Name"})
    Password      = PasswordField('Old Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    NewPassword   = PasswordField('New Password', validators=[Optional(), passwordPolicy, Length(min=8, message="Password must be 8 characters or more")], render_kw={"placeholder": "New Password"})
    NewPasswordx2 = PasswordField('Reenter New Password', validators=[EqualTo('NewPassword', message="Passwords must match")], render_kw={"placeholder": "Reenter New Password"})


# Form to edit a user's details as a manager
class ManagerForm(FlaskForm):
    Name          = StringField('Name', render_kw={"placeholder": "Name"})
    Email         = EmailField('email', render_kw={"placeholder": "Email"})
    NewPassword   = PasswordField('New Password', validators=[Optional(), Length(min=8, message="Passwords must be 8 characters or more")], render_kw={"placeholder": "New Password"})
    NewPasswordx2 = PasswordField('Reenter New Password', validators=[EqualTo('NewPassword', message="Passwords must match")], render_kw={"placeholder": "Reenter New Password"})
    Type        = IntegerField('Type', validators=[Optional(), NumberRange(min=1, max=3, message="Type must be 1, 2 or 3")], render_kw={"placeholder": "Type"})


# Form for analysis usage and sales
class AnalysisForm(FlaskForm):
    DateOf    = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(message="Please enter a Date")], render_kw={"placeholder": "Date of activity"})
    Facility    = StringField("Facility", render_kw={"placeholder": "Facility"}) 


# Form for editing discount amount
class DiscountForm(FlaskForm):
    DiscountAmount = IntegerField('Discount', validators=[DataRequired(message="Enter a discount amount")], render_kw={"placeholder": "Amount"})