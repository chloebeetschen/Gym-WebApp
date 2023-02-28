from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField, SubmitField, SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Length
from .models import Activity, Calendar

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
    cTime = SelectField('cTime', choices = [('07:00','07:00'), ('07:30','07:30'), ('08:00','08:00'), ('08:30','08:30'), ('09:00','09:00'), ('09:30','09:30'), ('10:00','10:00'), ('10:30','10:30'), ('11:30','11:00'), ('11:30','11:30'), ('12:00','12:00'), ('12:30','12:30'), ('13:00','13:00'), ('13:30','13:30'), ('14:00','14:00'), ('14:30','14:30'), ('15:00','15:00'), ('15:30','15:30'), ('16:00','16:00'), ('16:30','16:30'), ('17:00','17:00'), ('17:30','17:30'), ('18:00','18:00'), ('18:30','18:30'), ('19:00','19:00'), ('19:30','19:30'), ('20:00','20:00'), ('20:30','20:30'), ('21:00','21:00'), ('21:30','21:30')], validators=[DataRequired()])

    cDuration = SelectField('cDuration', choices = [(30, '30mins'), (60, '60mins')], validators=[DataRequired()])
    cFull = BooleanField('cFull')
    cCurrent = IntegerField('cCurrent')

    choicesType = [(a.id, a.activityType) for a in Activity.query.all()]
    cType = SelectField('cType', coerce=int, choices = choicesType, validators=[DataRequired()])

    #addEvent = SubmitField('addEvent')




