from app import db
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

class User(db.Model):
	__table_args__ = (
		CheckConstraint('email LIKE \'%_@_%._%\''),
	)
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	public = db.Column(db.Boolean(), nullable=False)
	trips = db.relationship('Trip', backref='user', lazy=True)

	def __init__(self, uid, username, email, password, public):
		self.uid = uid
		self.username = username
		self.email = email
		self.password = password
		self.public = public

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.uid

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Trips(db.Model):
	tid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey('user.uid', ondelete="CASCADE"), nullable=False)
	trip_name = db.Column(db.String(30), default="Trip Created on " + str(datetime.now()), nullable=False)
	details = db.relationship('Details', backref='trips', lazy=True)

	def __repr__(self):
		return '<Trips {}>'.format(self.tid)

	## TODO: validate that the trip names are unique per user


class Airlines(db.Model):
	iata = db.Column(db.String(2), primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	flights = db.relationship('Flights', backref='airlines', lazy=True)

	def __repr__(self):
		return '<Airlines {}>'.format(self.iata)


class Airports(db.Model):
	__table_args__ = (
		CheckConstraint('latitude >= -90 AND latitude <= 90'),
		CheckConstraint('longitude >= -180 AND longitude <= 180'),
		CheckConstraint('dst IN (\'E\', \'A\', \'S\', \'O\', \'Z\', \'N\', \'U\')'),
	)
	iata = db.Column(db.String(3), primary_key=True)
	name = db.Column(db.String(75), nullable=False)
	city = db.Column(db.String(75), nullable=False)
	country = db.Column(db.String(50), nullable=False)
	latitude = db.Column(db.Float(), nullable=False)
	longitude = db.Column(db.Float(), nullable=False)
	time_zone = db.Column(db.String(60), nullable=False)
	dst = db.Column(db.String(1), nullable=False)
	flights = db.relationship('Flights', backref='airports', lazy=True)

	def __repr__(self):
		return '<Airports {}>'.format(self.iata)

	## TODO: we don't need to verify the long, lat, and dst right? bc the airport data is waht we are entering and should be valid


class Flights(db.Model):
	__table_args__ = (
		CheckConstraint('flight_num > 0'),
		CheckConstraint('duration > 0'),
		CheckConstraint('mileage > 0'),
	)
	fid = db.Column(db.Integer, primary_key=True)
	tid = db.Column(db.Integer, db.ForeignKey('trips.tid', ondelete="CASCADE"), nullable=False)
	airline_iata = db.Column(db.String(2), db.ForeignKey('airlines.iata'))
	flight_num = db.Column(db.Integer) ##TODO: does this need to be >0?
	depart_iata = db.Column(db.String(3), db.ForeignKey('airports.iata', ondelete="CASCADE"), nullable=False)
	arrival_iata = db.Column(db.String(3), db.ForeignKey('airports.iata', ondelete="CASCADE"), nullable=False)
	depart_datetime = db.Column(db.DateTime, nullable=False)
	arrival_datetime = db.Column(db.DateTime, nullable=False)
	duration = db.Column(db.Integer, nullable=False)
	mileage = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<Flights {}>'.format(self.fid)


class Details(db.Model):
	did = db.Column(db.Integer, primary_key=True)
	tid = db.Column(db.Integer, db.ForeignKey('trips.tid', ondelete="CASCADE"), nullable=False)
	iata = db.Column(db.String(3), db.ForeignKey('airports.iata', ondelete="CASCADE"), nullable=False)
	note = db.Column(db.String(500), nullable=False)

	def __repr__(self):
		return '<Details {}>'.format(self.did)
