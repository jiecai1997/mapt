from app import app, bcrypt
from flask import render_template, flash, redirect, url_for, session, request
from app.forms import LoginForm, RegisterForm, FlightsForm, TripsForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3 as sql
from flask import jsonify
import random
from datetime import datetime
import math
import json

# json routes
@app.route('/login/register', methods=['POST'])
def register_user():
	json = request.get_json()

	username = json['username']
	email = json['email']
	password = json['hashedPassword']
	is_public = json['public']

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()

		# CHECK - if username or password already exists
		c = cur.execute("SELECT * FROM user WHERE username=(?) OR email=(?)", (username, email))
		urow = c.fetchone()

		# FAILURE - username or password already exists
		if urow:
			cur.close()
			return jsonify({'success': 'false', 'reason': 'username exists OR email exists'})

		# SUCCESS - no duplicate entries, add user to database
		cur.execute("INSERT INTO user (username, email, password, public) VALUES (?,?,?,?)",(username, email, password, is_public))
		con.commit()
		cur.close()
		return jsonify({'success': 'true'})

@app.route('/login/loginattempt', methods=['POST'])
def login_attempt():
	json = request.get_json()

	input_email = json['email']
	input_password = json['hashedPassword']

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT uid, username, email, password from user where email = (?)", [input_email])
		urow = c.fetchone()

		# fail - no user exists
		if urow is None:
			return jsonify({'success': 'false', 'reason': 'no user exists with this email'})

		db_uid = urow[0]
		db_username = urow[1]
		db_email = urow[2]
		db_password = urow[3]

		# success - user exists
		if input_email == db_email and input_password == db_password:
			session_token = input_email+str(random.randint(0, 1000))
			cur.execute("UPDATE user SET session = (?) WHERE email = (?)", [session_token, input_email])
			con.commit()
			cur.close()
			return jsonify({
					'success': 'true',
					'userid': db_uid,
					'sessionToken': session_token,
					'username': db_username
				})

		# fail - wrong password for user
		else:
			cur.close()
			return jsonify({'success': 'false', 'reason': 'wrong password'}) # TODO: ERROR CHECKING

# check if a user is logged in
@app.route('/login/verify/<int:uid>', methods=['GET'])
def verify_user(uid):
	input_token = request.headers.get('Authorization')
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session from user where uid = (?)", [uid])
		urow = c.fetchone()
		cur.close()

		# SUCCESS - if login token for user stored in database = header token
		if urow[0] == input_token:
			return jsonify({'loggedIn': 'true'})
		# FAILURE - if login token for user stored in database != header token
		else:
			return jsonify({'loggedIn': 'false'})


@app.route('/profile/<int:uid>', methods=['POST'])
def display_profile(uid):
	session_token = request.headers.get('Authorization')

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session, username, public from user where uid = (?)", [uid])
		urow = c.fetchone()

		# you do not have permission to change this
		if urow is None or urow[0] != session_token:
			con.commit()
			cur.close()
			return jsonify({'success': 'false'})

		# success - user exists
		username = urow[1]
		isPublic = urow[2]

		cur.commit()
		cur.close()
		return jsonify({
					'success': 'true',
					'username': username,
					'isPublic': isPublic
				})


@app.route('/profile/update', methods=['POST'])
def update_profile():
	json = request.get_json()
	session_token = request.headers.get('Authorization')

	uid = json['uid']
	username = json['username']
	isPublic = json['isPublic']

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session from user where uid = (?)", [uid])
		urow = c.fetchone()

		# you do not have permission to change this
		if urow is None or urow[0] != session_token:
			con.commit()
			cur.close()
			return jsonify({'success': 'false'})

		cur.execute("UPDATE user SET username = (?), isPublic = (?) WHERE uid = (?)", [username, isPublic, uid])
		result = cur.fetchall
		con.commit()
		cur.close()

		trip_stats = []
		for row in result:
  			trip_stats.append(row)

		return jsonify({'success': 'true', 'stats': trip_stats})


@app.route('/stats/<int:uid>', methods=['GET'])
def getstats_user(uid):
	json = request.get_json()
	session_token = request.headers.get('Authorization')
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session from user where uid = (?)", [uid])
		urow = c.fetchone()

		# you do not have permission to change this
		if urow is None or urow[0] != session_token:
			con.commit()
			cur.close()
			return jsonify({'success': 'false'})

		stats_per_trip = cur.execute("SELECT trip_name, SUM(mileage), SUM(duration) FROM Trip NATURAL JOIN Flight WHERE uid = (?) GROUP BY tid",[uid])
		con.commit()
		cur.close()
		return jsonify({'stats': [{'title': 'stat1', 'value':1000}, {'title': 'stat2', 'value':2000}]})


@app.route('/trips/add', methods=['POST'])
def addtrip_user():
	json = request.get_json()
	session_token = request.headers.get('Authorization')

	uid = json['uid']
	trip_name = json['trip_name']
	color = json['color']
	flights = json['flights']
	monthdic = {'01':'Jan', '02':'Feb','03':'Mar', '04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

	def deg2rad(deg):
		return abs(deg * (math.pi/180))

	def LatLonToMiles(lat1,lon1,lat2,lon2):
		R = 3958.8 #Radius of the earth in miles
		dLat = deg2rad(lat2-lat1)
		dLon = deg2rad(lon2-lon1)
		a = math.sin(dLat/2)**2 + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		d = R * c #Distance in miles
		return int(d)


	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session from user where uid = (?)", [uid])
		urow = c.fetchone()

		# you do not have permission to change this
		if urow is None or urow[0] != session_token:
			con.commit()
			cur.close()
			return jsonify({'success': 'false'})

		tid = cur.execute("INSERT INTO trip (uid, trip_name,color) VALUES (?,?,?)",(uid, trip_name,color))
		tid = tid.lastrowid

		for flight in flights:
			arrival_iata = flight['arr']['airport']
			arrival_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = (?)",[arrival_iata]).fetchone()
			arrival_tz = arrival_airport["time_zone"]
			arrival_lat = arrival_airport["latitude"]
			arrival_long = arrival_airport["longitude"]

			depart_iata = flight['dep']['airport']
			depart_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = (?)",[depart_iata]).fetchone()
			depart_tz = depart_airport["time_zone"]
			depart_lat = depart_airport["latitude"]
			depart_long = depart_airport["longitude"]

			airline_iata = 'AA' #Hardcode for now
			flight_num = 1 #Hardcode for now

			print('flight')
			print(flight)

			depart_date = flight['dep']['date'].split("T")[0].split("-")
			print('depart_date')
			print(depart_date)
			depart_mth = depart_date[1]
			depart_day = depart_date[2]
			depart_yr = depart_date[0]
			depart_hr = int(flight['dep']['time'].split(':')[0])
			int_depart_hr = depart_hr
			depart_min = flight['dep']['time'].split(':')[1]
			depart_ampm = 'AM'
			if depart_hr >= 12:
				depart_hr-=12
				depart_ampm = 'PM'
			depart_datetime = depart_yr+depart_mth+depart_day+' '+str(depart_hr)+':'+depart_min+':00 '+depart_ampm
			dt_depart_datetime = datetime(int(depart_yr),int(depart_mth),int(depart_day),int_depart_hr,int(depart_min))

			arr_date = flight['arr']['date'].split("T")[0].split("-")
			arr_mth = arr_date[1]
			arr_day = arr_date[2]
			arr_yr = arr_date[0]
			arr_hr = int(flight['arr']['time'].split(':')[0])
			int_arr_hr = arr_hr
			arr_min = flight['arr']['time'].split(':')[1]
			arr_ampm = 'AM'
			if arr_hr >= 12:
				arr_hr-=12
				arr_ampm = 'PM'
			arrival_datetime = arr_yr+arr_mth+arr_day+' '+str(arr_hr)+':'+arr_min+':00 '+arr_ampm
			dt_arr_datetime = datetime(int(arr_yr),int(arr_mth),int(arr_day),int_arr_hr,int(arr_min))

			duration = (dt_arr_datetime-dt_depart_datetime).seconds//60
			offset_mins = int((float(depart_tz)-float(arrival_tz))*60)
			duration += offset_mins

			mileage = LatLonToMiles(depart_lat,depart_long,arrival_lat,arrival_long)

			cur.execute("INSERT INTO flight (tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage) VALUES (?,?,?,?,?,?,?,?,?)",(tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage))
		con.commit()
		cur.close()
		return jsonify({'success': 'true'})

@app.route('/trips/<int:uid>', methods=['GET'])
def gettrips_user(uid):
	json = request.get_json()
	session_token = request.headers.get('Authorization')

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session from user where uid = (?)", [uid])
		urow = c.fetchone()

		# you do not have permission to change this
		if urow is None or urow[0] != session_token:
			con.commit()
			cur.close()
			return jsonify({'success': 'false'})

		cur.execute("SELECT * FROM trip WHERE uid = (?)",[uid])
		triprows = cur.fetchall()
		ret = []
		for row in triprows:
			d = {}
			d['userid']=row['uid']
			d['tripid']=row['tid']
			d['tripName']=row['trip_name']
			d['color']=row['color']
			d['flights'] = []
			cur.execute("SELECT * FROM flight WHERE tid = (?)",[row['tid']])
			flightrows = cur.fetchall()
			for flight in flightrows:
				depart_iata = flight['depart_iata']
				depart_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = (?)",[depart_iata]).fetchone()
				depart_datetime = flight['depart_datetime']

				arrival_iata = flight['arrival_iata']
				arrival_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = (?)",[arrival_iata]).fetchone()
				arrival_datetime = flight['arrival_datetime']

				flightdic = {}
				flightdic['color']=row['color']

				flightdic['departAirport']= depart_iata
				depart_datetime_split = depart_datetime.split(" ")
				flightdic['depart_date'] = depart_datetime_split[0]
				flightdic['depart_time'] = depart_datetime_split[1] + " " + depart_datetime_split[2]

				flightdic['arrivalAirport']= arrival_iata
				arrival_datetime_split = arrival_datetime.split(" ")
				flightdic['arrival_date'] = arrival_datetime_split[0]
				flightdic['arrival_time'] = arrival_datetime_split[1] + " " + arrival_datetime_split[2]

				d['flights'].append(flightdic)
			ret.append(d)
		con.commit()
		cur.close()
		return jsonify({'success': True,'trips': ret})


@app.route('/trips/update', methods=['POST'])
def updatetrip_user():
	json = request.get_json()
	session_token = request.headers.get('Authorization')

	uid = json['uid']
	trip_name = json['trip_name']
	tid = json['tripID']
	color = json['color']
	flights = json['flights']
	monthdic = {'01':'Jan', '02':'Feb','03':'Mar', '04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

	def deg2rad(deg):
		return abs(deg * (math.pi/180))

	def LatLonToMiles(lat1,lon1,lat2,lon2):
		R = 3958.8 #Radius of the earth in miles
		dLat = deg2rad(lat2-lat1)
		dLon = deg2rad(lon2-lon1)
		a = math.sin(dLat/2)**2 + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		d = R * c #Distance in miles
		return int(d)


	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session from user where uid = (?)", [uid])
		urow = c.fetchone()

		# you do not have permission to change this
		if urow is None or urow[0] != session_token:
			con.commit()
			cur.close()
			return jsonify({'success': 'false'})

		cur.execute("DELETE FROM trip WHERE tid = (?)",[tid])
		cur.execute("DELETE FROM flight WHERE tid = (?)",[tid])
		tid = cur.execute("INSERT INTO trip (uid, trip_name,color) VALUES (?,?,?)",(uid, trip_name,color))
		tid = tid.lastrowid

		for flight in flights:
			arrival_iata = flight['arr']['airport']
			arrival_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = (?)",[arrival_iata]).fetchone()
			arrival_tz = arrival_airport["time_zone"]
			arrival_lat = arrival_airport["latitude"]
			arrival_long = arrival_airport["longitude"]

			depart_iata = flight['dep']['airport']
			depart_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = (?)",[depart_iata]).fetchone()
			depart_tz = depart_airport["time_zone"]
			depart_lat = depart_airport["latitude"]
			depart_long = depart_airport["longitude"]

			airline_iata = 'AA' #Hardcode for now
			flight_num = 1 #Hardcode for now

			print('flight')
			print(flight)

			depart_date = flight['dep']['date'].split("T")[0].split("-")
			print('depart_date')
			print(depart_date)
			depart_mth = depart_date[1]
			depart_day = depart_date[2]
			depart_yr = depart_date[0]
			depart_hr = int(flight['dep']['time'].split(':')[0])
			int_depart_hr = depart_hr
			depart_min = flight['dep']['time'].split(':')[1]
			depart_ampm = 'AM'
			if depart_hr >= 12:
				depart_hr-=12
				depart_ampm = 'PM'
			depart_datetime = depart_yr+depart_mth+depart_day+' '+str(depart_hr)+':'+depart_min+':00 '+depart_ampm
			dt_depart_datetime = datetime(int(depart_yr),int(depart_mth),int(depart_day),int_depart_hr,int(depart_min))

			arr_date = flight['arr']['date'].split("T")[0].split("-")
			arr_mth = arr_date[1]
			arr_day = arr_date[2]
			arr_yr = arr_date[0]
			arr_hr = int(flight['arr']['time'].split(':')[0])
			int_arr_hr = arr_hr
			arr_min = flight['arr']['time'].split(':')[1]
			arr_ampm = 'AM'
			if arr_hr >= 12:
				arr_hr-=12
				arr_ampm = 'PM'
			arrival_datetime = arr_yr+arr_mth+arr_day+' '+str(arr_hr)+':'+arr_min+':00 '+arr_ampm
			dt_arr_datetime = datetime(int(arr_yr),int(arr_mth),int(arr_day),int_arr_hr,int(arr_min))

			duration = (dt_arr_datetime-dt_depart_datetime).seconds//60
			offset_mins = int((float(depart_tz)-float(arrival_tz))*60)
			duration += offset_mins

			mileage = LatLonToMiles(depart_lat,depart_long,arrival_lat,arrival_long)

			cur.execute("INSERT INTO flight (tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage) VALUES (?,?,?,?,?,?,?,?,?)",(tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage))
		con.commit()
		cur.close()
		return jsonify({'success': 'true'})

# DEPRECATED, refer to flights/uid
@app.route('/flights', methods=['GET', 'POST'])
def flights():
	if request.method == 'GET':
		json = request.get_json()
		print('headers')
		print(request.headers)

		# username = json['userid']
		# STILL NEED TO PERFORM TOKEN VALIDATION IN ALL ROUTES, CHECK IF USER ID IS PRIVATE IF NOT

		with sql.connect("app.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			cur.execute("SELECT departAirports.Latitude AS deptLat, departAirports.Longitude AS deptLong, arriveAirports.Latitude as arrLat, arriveAirports.Longitude as arrLong FROM flight, airport AS departAirports, airport AS arriveAirports WHERE flight.depart_iata = departAirports.IATA AND flight.arrival_iata = arriveAirports.IATA")
			flightRows = cur.fetchall()
		print(flightRows)
		flights = []
		for flight in flightRows:
			# NEED TO FETCH CORRECT COLOR BY JOINING WITH TRIP - RIGHT NOW, HARDCODED WITH HOTPINK
			tempDict = {'firstPointLat': flight['deptLat'], 'firstPointLong': flight['deptLong'], 'secondPointLat': flight['arrLat'], 'secondPointLong': flight['arrLong'], 'color':'hotpink'}
			flights.append(tempDict)
		print('here')

		print(flights)
		# return jsonify({'flights': flights, 'success': 'true'})
		return jsonify({'flights': [{'firstPointLat': 42, 'firstPointLong': 42, 'secondPointLat': 21, 'secondPointLong': 21, 'color':'lime'}], 'success': 'true'})
	else: # request method is a POST
		return {}

@app.route('/flights/<int:uid>', methods=['GET'])
def get_flights(uid):
	input_token = request.headers.get('Authorization')

	# FAIL - if none or invalid input token
	if input_token is None:
		return jsonify({
			'success': 'false',
			'reason': 'none or invalid session token'
		})

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT session, public from user where uid = (?)", [uid])
		urow = c.fetchone()
		requested_token = urow[0]
		requested_public = urow[1]
		# FAIL - if current user token != requested user token and requested user profile is private
		if input_token != requested_token and requested_public == 0:
			cur.close()
			return jsonify({
				'success': 'false',
				'reason': 'account is private'
			})

		# OTHERWISE SUCCESS, TODO - get all flights from requested user
		c = cur.execute(
			'''
			SELECT
				t.color
				, depart_a.latitude
				, depart_a.longitude
				, arrival_a.latitude
				, arrival_a.longitude
			FROM flight f JOIN trip t ON f.tid = t.tid
			JOIN airport depart_a ON f.depart_iata = depart_a.iata
			JOIN airport arrival_a ON f.arrival_iata = arrival_a.iata
			WHERE t.uid = (?)
			'''
			, [uid]
		)
		flights = c.fetchall()
		cur.close()
		flights_arr = []

		for flight in flights:

			color = flight[0]
			depart_lat = flight[1]
			depart_long = flight[2]
			arrival_lat = flight[3]
			arrival_long = flight[4]

			flights_arr.append({
				'color':color
				, 'firstPointLat':depart_lat
				, 'firstPointLong':depart_long
				, 'secondPointLat':arrival_lat
				, 'secondPointLong':arrival_long
			})

		return jsonify({
			'success': 'true',
			'flights': flights_arr
		})


# @app.route('/trips', methods=['GET', 'POST'])
# def trips():
# 	form = TripsForm(request.form)
# 	if request.method == 'POST' and form.validate():
# 		uid = form.uid.data
# 		trip_name = form.trip_name.data
# 		with sql.connect("app.db") as con:
# 			con.row_factory = sql.Row
# 			cur = con.cursor()
# 			cur.execute("INSERT INTO trip (uid, trip_name) VALUES (?,?)",(uid, trip_name))
# 			con.commit()
# 			cur.close()
# 			flash('You Added A Trip!')
# 			return redirect('/list')
# 	return {'trips':[]}

@app.route('/list')
def list():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("select * from user")
		userrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from trip")
		tripsrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from airline")
		airlinesrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from airport")
		airportsrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from flight")
		flightsrows = cur.fetchall()
		cur.close()
	return render_template("list.html",userrows = userrows,tripsrows = tripsrows,
    airlinesrows = airlinesrows, airportsrows = airportsrows, flightsrows = flightsrows)

# janky updates here!!!
@app.route('/update')
def update():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()

		# add user
		cur.execute(
			'''
			INSERT INTO
			user(uid, username, email, password, public, session)
			VALUES(4, 'alpaca', 'alpaca@gmail.com', 'llamallamallama', 1, 'alpaca1')
			'''
		)

		'''
		# add trip
		cur.execute(
			INSERT INTO
			trip(tid, uid, trip_name, color)
			VALUES(17,2,'llama', 'red')

		)
		cur.execute(

			INSERT INTO
			trip(tid, uid, trip_name, color)
			VALUES(18,2,'alpaca', 'purple')
		)

		# add flight
		cur.execute(
			INSERT INTO
			flight(fid, tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage)
			VALUES(3,17,'DL',695, 'EWR', 'SFO', '2007-02-01 10:00:00', '2007-02-01 12:00:00', 180, 600)
		)
		cur.execute(
			INSERT INTO
			flight(fid, tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage)
			VALUES(4,17,'DL',659, 'SFO', 'EWR', '2007-03-01 10:00:00', '2007-03-01 12:00:00', 180, 600)
		)
		cur.execute(
			INSERT INTO
			flight(fid, tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage)
			VALUES(5,18,'DL',849, 'SFO', 'EWR', '2007-03-01 10:00:00', '2007-03-01 12:00:00', 180, 600)
		)

		#add airport
		cur.execute(
			INSERT INTO
			airport(iata, name, city, country, latitude, longitude, time_zone, dst)
			VALUES ('EWR', 'Newark Airport', 'Newark', 'USA', 96, 96, 'EST', 'EST')
		)

		# add airline
		cur.execute(
			INSERT INTO
			airline(iata, name)
			VALUES('DL', 'Delta Airlines')
		)
		'''

		con.commit()
		cur.close()
	return render_template('home.html')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
   app.run(debug = True)
