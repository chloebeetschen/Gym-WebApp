from flask_wtf import FlaskForm
import datetime
from wtforms import PasswordField, EmailField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField
from wtforms import StringField, BooleanField, IntegerField 
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

#for the manager to add a new activity e.g. swimming
class addActivityForm(FlaskForm):
    aType      = StringField('aType', validators=[DataRequired()])
    aPrice     = IntegerField('aPrice', validators=[DataRequired()])
    aLocation  = StringField('aLocation', validators=[DataRequired()])
    aCapacity  = IntegerField('aCapacity', validators=[DataRequired()])
    aStaffName = StringField('aStaffName', validators=[DataRequired()])

    addActivity = SubmitField('addActivity')

#for the manager to edit an activity e.g. swimming
class editActivityForm(FlaskForm):
    aPrice = IntegerField('aPrice')
    aLocation = StringField('aLocation')
    aCapacity = IntegerField('aCapacity')
    aStaffName = StringField('aStaffName')

    editActivity = SubmitField('editActivity')


#for the manager to add a new event  e.g. swimming at a new location/time
class addEventForm(FlaskForm):
    cDate = DateField('cDate', validators=[DataRequired()])
    #manager can select a time in 30 min increments 
    cTime = SelectField('cTime', choices=timeChoices, validators=[DataRequired()])

    cDuration = SelectField('cDuration', choices = [(30, '30mins'), (60, '60mins')], validators=[DataRequired()])
    cFull = BooleanField('cFull')
    cCurrent = IntegerField('cCurrent')

    #choicesType = [(a.id, a.activityType) for a in Activity.query.all()]
    #cType = SelectField('cType', coerce=int, choices = choicesType, validators=[DataRequired()])
    addEvent = SubmitField('addEvent')


#for the manager to edit an  event  e.g. swimming at a new location/time
class editEventForm(FlaskForm):
    cDate = DateField('cDate')
    #manager can select a time in 30 min increments 
    cTime = SelectField('cTime', choices = timeChoices)
    cDuration = SelectField('cDuration', choices = [(30, '30mins'), (60, '60mins')])

    editEvent = SubmitField('editEvent')


# function to check that card number is a Luhn number
def validateLuhn(form, field):
     if verify(str(field.data)) == False:
         raise ValidationError('Card Number is not valid')


# function to check expiry date is in the future
def validateExpiry(form, field):
    if field.data < datetime.date.today():
        raise ValidationError('The card has expired')


# form to create account:
class PaymentForm(FlaskForm):
    cName = StringField('Name', validators=[DataRequired()])
    cNum = IntegerField('Card number',
                        validators=[DataRequired(message='Please enter a card number'), 
                        NumberRange(min=1000000000000000, max=9999999999999999, message='Card number needs to be 16 digits'),
                        validateLuhn])

    cExpDate = DateField('Expiry',
                         validators=[DataRequired(message='Please enter an expiry date'),
                         validateExpiry])

    cCVV = IntegerField('CVV', 
                         validators=[DataRequired(message='Please enter the CVV'),
                         NumberRange(min=100, 
                         max=999,
                         message='CVV needs to be 3 digits')])


class RegisterForm(FlaskForm):
    Name        = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    DateOfBirth = DateField('Date of birth', validators=[DataRequired()], render_kw={"placeholder": "Date of Birth"})
    Address     = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    Email       = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password    = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    Type        = IntegerField('Type', validators=[DataRequired(), NumberRange(min=1, max=3)])

class LoginForm(FlaskForm):
    Email    = EmailField('email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})

class SettingsForm(FlaskForm):
    Name        = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    DateOfBirth = DateField('Date of birth', validators=[DataRequired()], render_kw={"placeholder": "Date of Birth"})
    Address     = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    Email       = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password    = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    NewPassword = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "New Password"})