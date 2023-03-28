from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField, DateTimeLocalField
from wtforms import StringField, BooleanField, IntegerField, FloatField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError, Optional
from datetime import *

# Function to check that a date is in the future
def validateFutureDate(form, field):
    if field.data < datetime.now():
        raise ValidationError('You must enter a date in the future')


# Function to check that registree is old enough to register
def validateAge(form, field):
    oldEnough = datetime.now().date()-timedelta(days=16*365)
    if field.data > oldEnough:
        raise ValidationError("You are not old enough to register")

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


#Search for a user
class SearchForm(FlaskForm):
    search       = StringField('Search')


# Form to add an activity to the calendar
# Can be used for editing and adding calendar events
class EventForm(FlaskForm):
    aDateTime    = DateTimeLocalField('Date & Time of activity', format='%Y-%m-%dT%H:%M', validators=[DataRequired(), validateFutureDate], render_kw={"placeholder": "Date of activity"})
    aDuration    = IntegerField('Duration of activity', validators=[DataRequired(), NumberRange(min=0)],
                             render_kw={"placeholder": "Duration of activity"})
    aStaffName   = StringField("Staff Name", validators=[DataRequired()], render_kw={"placeholder": "Staff Member"}) 
    aLocation    = StringField("Location", validators=[DataRequired()], render_kw={"placeholder": "Location"}) 
    aPrice       = FloatField("Price", validators=[NumberRange(min=0.0), DataRequired()], render_kw={"placeholder": "Price of activity"}) 
    aCapacity    = IntegerField('Capacity of activity', validators=[ NumberRange(min=0), DataRequired()],
                               render_kw={"placeholder": "Capacity of activity"})


class RegisterForm(FlaskForm):
    Name        = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    DateOfBirth = DateField('Date of birth', validators=[DataRequired(), validateAge], render_kw={"placeholder": "Date of Birth"})
    Email       = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password    = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be 8 characters or more"), passwordPolicy], render_kw={"placeholder": "Password"})
    ReenterPassword = PasswordField('Reenter Password', validators=[DataRequired(), 
                                                                    EqualTo('Password', message="Passwords must match" )],
                                                                    render_kw={"placeholder": "Reenter Password"})
    Type        = IntegerField('Type', validators=[DataRequired(), NumberRange(min=1, max=3)], render_kw={"placeholder": "Type"})


class LoginForm(FlaskForm):
    Email       = EmailField('email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password    = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})


class SettingsForm(FlaskForm):
    Name          = StringField('Name', render_kw={"placeholder": "Name"})
    Password      = PasswordField('Old Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    NewPassword   = PasswordField('New Password', validators=[Optional(), passwordPolicy, Length(min=8, message="Password must be 8 characters or more")], render_kw={"placeholder": "New Password"})
    NewPasswordx2 = PasswordField('Reenter New Password', validators=[EqualTo('NewPassword', message="Passwords must match")], render_kw={"placeholder": "Reenter New Password"})

class ManagerForm(FlaskForm):
    Name          = StringField('Name', render_kw={"placeholder": "Name"})
    Email         = EmailField('email', render_kw={"placeholder": "Email"})
    NewPassword   = PasswordField('New Password', validators=[Optional(), Length(min=8, message="Passwords must be 8 characters or more")], render_kw={"placeholder": "New Password"})
    NewPasswordx2 = PasswordField('Reenter New Password', validators=[EqualTo('NewPassword', message="Passwords must match")], render_kw={"placeholder": "Reenter New Password"})
    Type        = IntegerField('Type', validators=[Optional(), NumberRange(min=1, max=3, message="Type must be 1, 2 or 3")], render_kw={"placeholder": "Type"})


class AnalysisForm(FlaskForm):
    #need to add some type of validation here: latest date chosen can be 7 days prior to todays date
    DateOf    = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(message="Please enter a Date")], render_kw={"placeholder": "Date of activity"})
    Facility    = StringField("Facility", render_kw={"placeholder": "Facility"}) 
