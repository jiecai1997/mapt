from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateTimeField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class FlightsForm(FlaskForm):
    fid = IntegerField('Fid')
    tid = IntegerField('Tid')
    airline_iata = StringField('Airline Code', [validators.Length(min=2, max=3)])
    flight_num = IntegerField('Flight Number')
    depart_iata = StringField('Departure Airport', [validators.Length(min=3, max=4)])
    arrival_iata = StringField('Arrival Airport', [validators.Length(min=3, max=4)])
    depart_datetime = DateTimeField('Departure Date & Time')
    arrival_datetime = DateTimeField('Arrival Date & Time')
    duration = IntegerField('Duration/hr')
    mileage = IntegerField('Mileage')
    submit = SubmitField('Create Flight')
