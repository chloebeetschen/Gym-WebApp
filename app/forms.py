from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, EmailField, DateField, PasswordField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    DateOfBirth = DateField('Date of birth', validators=[DataRequired()], render_kw={"placeholder": "Date of Birth"})
    Address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    Email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})


class LoginForm(FlaskForm):
    Email = EmailField('email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    Password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})