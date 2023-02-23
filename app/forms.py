from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, EmailField, DateField, PasswordField
from wtforms.validators import DataRequired

class Register(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dateOfBirth = DateField('Date of birth', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
class Login(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])