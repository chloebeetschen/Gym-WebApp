from flask_wtf import FlaskForm
from flask import flash
import datetime
from wtforms import StringField, PasswordField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, ValidationError
from app import app
from luhn import *

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
    cNum = IntegerField('Card number', validators=[DataRequired(message='Please enter a card number'), NumberRange(min=1000000000000000, max=9999999999999999, message='Card number needs to be 16 digits'), validateLuhn])
    cExpDate = DateField('Expiry', validators=[DataRequired(message='Please enter an expiry date'), validateExpiry])
    cCVV = IntegerField('CVV', validators=[DataRequired(message='Please enter the CVV'), NumberRange(min=100, max=999, message='CVV needs to be 3 digits')])

