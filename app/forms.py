from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Length
from .models import Activity

#for the manager to add a new activity e.g. swimming
class addActivityForm(FlaskForm):
    aType = StringField('aType', validators=[DataRequired()])
    aPrice = IntegerField('aPrice', validators=[DataRequired()])
    aLocation = StringField('aLocation', validators=[DataRequired()])
    aCapacity = IntegerField('aCapacity', validators=[DataRequired()])
    aStaffName = StringField('aStaffName', validators=[DataRequired()])

    addActivity = SubmitField('addActivity')

#for the manager to add a new event  e.g. swimming at a new location/time
class addEventForm(FlaskForm):
    cDate = DateField('cDate', validators=[DataRequired()])
    #manager can select a time in 30 min increments 
    cTime = SelectField('cTime', choices = [(700,'07:00'), (730,'07:30'), (800,'08:00'), (830,'08:30'), (900,'09:00'), (900,'09:30'), (1000,'10:00'), (1030,'10:30'), (1100,'11:00'), (1130,'11:30'), (1200,'12:00'), (1230,'12:30'), (1300,'13:00'), (1330,'13:30'), (1400,'14:00'), (1430,'14:30'), (1500,'15:00'), (1530,'15:30'), (1600,'16:00'), (1630,'16:30'), (1700,'17:00'), (1730,'17:30'), (1800,'18:00'), (1830,'18:30'), (1900,'19:00'), (1930,'19:30'), (2000,'20:00'), (2030,'20:30'), (2100,'21:00'), (2130,'21:30')], validators=[DataRequired()])

    cDuration = SelectField('cDuration', choices = [(30, '30mins'), (60, '60mins')], validators=[DataRequired()])
    cFull = BooleanField('cFull', validators=[DataRequired()])
    cCurrent = IntegerField('cCurrent', validators=[DataRequired()])

    #choicesType = [(a.activityType) for a in Sports.query.all()]
    cType = SelectField('cType', choices = {(700,'07:00'), (730,'07:30')}, validators=[DataRequired()])

    addEvent = SubmitField('addEvent')




