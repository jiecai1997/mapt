from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FlightsForm(FlaskForm):
    fid = IntegerField('Fid')
    tid = IntegerField('Tid')
    airline_iata = StringField('Airline Code', [validators.Length(min=2, max=2)])
    flight_num = IntegerField('Flight Number')
    depart_iata = StringField('Departure Airport', [validators.Length(min=3, max=3)])
    arrival_iata = StringField('Arrival Airport', [validators.Length(min=3, max=3)])
    depart_datetime = DateTimeField('Departure Date & Time')
    arrival_datetime = DateTimeField('Arrival Date & Time')
    duration = IntegerField('Duration/hr')
    mileage = IntegerField('Mileage')
    submit = SubmitField('Create Flight')
