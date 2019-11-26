from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from datetime import datetime
from app import db


class User(db.Model):
	__table_args__ = (
		CheckConstraint('email LIKE \'%_@_%._%\''),
	)
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	public = db.Column(db.Boolean(), nullable=False)
	trip_rel = db.relationship('Trip', backref=db.backref('user', lazy=True))

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


class Trip(db.Model):
	tid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey('user.uid', ondelete="CASCADE"), nullable=False)
	trip_name = db.Column(db.String(30), default="Trip Created on " + str(datetime.now()), nullable=False)
	flight_rel = db.relationship('Flight', backref=db.backref('flight', lazy=True))
	detail_rel = db.relationship('Detail', backref=db.backref('trip', lazy=True))

	def __repr__(self):
		return '<Trip {}>'.format(self.tid)

	## TODO: validate that the trip names are unique per user


class Airline(db.Model):
	iata = db.Column(db.String(2), primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	flight_rel = db.relationship('Flight', backref=db.backref('airline', lazy=True))

	def __repr__(self):
		return '<Airline {}>'.format(self.iata)


class Airport(db.Model):
	# __table_args__ = (
	# 	CheckConstraint('latitude >= -90 AND latitude <= 90'),
	# 	CheckConstraint('longitude >= -180 AND longitude <= 180'),
	# 	CheckConstraint('dst IN (\'E\', \'A\', \'S\', \'O\', \'Z\', \'N\', \'U\')'),
	# )
	iata = db.Column(db.String(3), primary_key=True)
	name = db.Column(db.String(75), nullable=False)
	city = db.Column(db.String(75), nullable=False)
	country = db.Column(db.String(50), nullable=False)
	latitude = db.Column(db.Float(), nullable=False)
	longitude = db.Column(db.Float(), nullable=False)
	time_zone = db.Column(db.String(60), nullable=False)
	dst = db.Column(db.String(1), nullable=False)
	aflight_rel = db.relationship('Flight', backref=db.backref('arrival', lazy=True), foreign_keys = 'Flight.arrival_iata')
	dflight_rel = db.relationship('Flight', backref=db.backref('depart', lazy=True), foreign_keys = 'Flight.depart_iata')
	detail_rel = db.relationship('Detail', backref=db.backref('airport', lazy=True))

	def __repr__(self):
		return '<Airport {}>'.format(self.iata)

	## TODO: we don't need to verify the long, lat, and dst right? bc the airport data is waht we are entering and should be valid


class Flight(db.Model):
	__table_args__ = (
		CheckConstraint('flight_num > 0'),
		CheckConstraint('duration > 0'),
		CheckConstraint('mileage > 0'),
	)
	fid = db.Column(db.Integer, primary_key=True)
	tid = db.Column(db.Integer, db.ForeignKey('trip.tid', ondelete="CASCADE"), nullable=False)
	airline_iata = db.Column(db.String(2), db.ForeignKey('airline.iata'))
	flight_num = db.Column(db.Integer)
	depart_iata = db.Column(db.String(3), db.ForeignKey('airport.iata', ondelete="CASCADE"), nullable=False)
	arrival_iata = db.Column(db.String(3), db.ForeignKey('airport.iata', ondelete="CASCADE"), nullable=False)
	depart_datetime = db.Column(db.DateTime, nullable=False)
	arrival_datetime = db.Column(db.DateTime, nullable=False)
	duration = db.Column(db.Integer, nullable=False)
	mileage = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<Flight {}>'.format(self.fid)


class Detail(db.Model):
	did = db.Column(db.Integer, primary_key=True)
	tid = db.Column(db.Integer, db.ForeignKey('trip.tid', ondelete="CASCADE"), nullable=False)
	iata = db.Column(db.String(3), db.ForeignKey('airport.iata', ondelete="CASCADE"), nullable=False)
	note = db.Column(db.String(500), nullable=False)

	def __repr__(self):
		return '<Detail {}>'.format(self.did)
