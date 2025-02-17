from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models import User

class LoginForm(FlaskForm):
    """
    Class handles the registering of an existing user. The varibales are defined using wtforms fields.
    The types taken by those fields are listed below.
    """
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    Class handles the registering of a new user. The varibales are defined using wtforms fields.
    The types taken by those fields are listed below.
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        """
        This function makes sure that the user is indeed a new user and not reinputing existing information within database.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetForm(FlaskForm):
    """
    Class handles the reseting of an existing user's information. This will remove the user.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    submit = SubmitField('Sign In')
