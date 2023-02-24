from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, EmailField, DateField, PasswordField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    dateOfBirth = DateField('Date of birth', validators=[DataRequired()], render_kw={"placeholder": "Date of Birth"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})