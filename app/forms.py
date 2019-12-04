from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models import User

"""
Contains all the FlaskForm's classes. 
"""

class LoginForm(FlaskForm):
"""Class for logging in a user."""
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
"""Class for registering new users"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
"""Verify the new users information is not already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetForm(FlaskForm):
"""Resets an old users information"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    submit = SubmitField('Sign In')
