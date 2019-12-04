from app import app, bcrypt
from flask import render_template, flash, redirect, url_for, session, request
from app.forms import LoginForm, RegisterForm, FlightsForm, TripsForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3 as sql
from flask import jsonify
import random

# json routes
@app.route('/user/register', methods=['POST'])
def register_user():
	json = request.get_json()

	username = json['username']
	email = json['email']
	password = json['hashedPassword']

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("INSERT INTO user (username, email, password, public) VALUES (?,?,?,?)",(username, email, password, 1))
		con.commit()
		cur.close()

		return jsonify({'success': 'true'}) # TODO: ADD ERROR CHECKING

@app.route('/login/loginattempt', methods=['POST'])
def login_attempt():
	json = request.get_json()

	input_email = json['email']
	input_password = json['hashedPassword']

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		c = cur.execute("SELECT username, email, password from user where email = (?)", [input_email])
		urow = c.fetchone()

		# fail - no user exists
		if urow is None:
			return jsonify({'success': 'false', 'reason': 'urow was None'})
		
		db_username = urow[0]
		db_email = urow[1]
		db_password = urow[2]

		# success - user exists
		if input_email == db_email and input_password == db_password:
			session_token = input_email+str(random.randint(0, 1000))
			cur.execute("UPDATE user SET session = (?) WHERE email = (?)", [session_token, input_email])
			con.commit()
			cur.close()
			# HARDCODED VALUE HERE NEEDS TO BE FIXED
			return jsonify({
					'success': 'true',
					'userid': 1234,
					'sessionToken': session_token,
					'username': db_username
				})

		# fail - wrong password for user
		else:
			cur.commit()
			cur.close()
			return jsonify({'success': 'false', 'reason': 'wrong password'}) # TODO: ERROR CHECKING


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
		con.commit()
		cur.close()
		return jsonify({'success': 'true'})


@app.route('/trips/add', methods=['POST'])
def addtrip_user():
	json = request.get_json()
	session_token = request.headers.get('Authorization')

	uid = json['uid']
	trip_name = json['trip_name']
	color = json['color']
	flights = json['flights']
	monthdic = {'Jan':'01', 'Feb':'02','Mar':'03', 'Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

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

		cur.execute("INSERT INTO trip (uid, trip_name,color) VALUES (?,?,?)",(uid, trip_name,color))
		#GET tid somehow!!!

		for flight in flights:
			arrival_iata = flight['arr']['airport']
			arrival_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = arrival_iata").fetchone()
			arrival_tz = arrival_airport["time_zone"]
			arrival_lat = arrival_airport["latitude"]
			arrival_long = arrival_airport["longitude"]

			depart_iata = flight['dep']['airport']
			depart_airport = cur.execute("SELECT * FROM airport WHERE airport.iata = depart_iata").fetchone()
			depart_tz = depart_airport["time_zone"]
			depart_lat = depart_airport["latitude"]
			depart_long = depart_airport["longitude"]

			airline_iata = 'AA' #Hardcode for now
			flight_num = 1 #Hardcode for now

			depart_date = flight['dep']['date'].split("00:")[0].split(" ")
			depart_mth = monthdic[depart_date[1]]
			depart_day = depart_date[2]
			depart_yr = depart_date[3]
			depart_hr = int(flight['dep']['time'].split(':'))[0]
			depart_min = flight['dep']['time'].split(':')[1]
			depart_ampm = 'AM'
			if depart_hr >= 12:
				depart_hr-=12
				depart_ampm = 'PM'
			depart_datetime = depart_yr+depart_mth+depart_date+' '+str(depart_hr)+':'+depart_min+':00'+depart_ampm

			arr_date = flight['arr']['date'].split("00:")[0].split(" ")
			arr_mth = monthdic[arr_date[1]]
			arr_day = arr_date[2]
			arr_yr = arr_date[3]
			arr_hr = int(flight['arr']['time'].split(':'))[0]
			arr_min = flight['arr']['time'].split(':')[1]
			arr_ampm = 'AM'
			if arr_hr >= 12:
				arr_hr-=12
				arr_ampm = 'PM'
			arrival_datetime = arr_yr+arr_mth+arr_date+' '+str(arr_hr)+':'+arr_min+':00'+arr_ampm

			duration = 5
			#Calculate with depart_datetime, arrival_datetime, & Timezone Data

			mileage = 5
			#Calculate with longitude & latitude
			#https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula

			cur.execute("INSERT INTO flight (tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage) VALUES (?,?,?,?,?,?,?,?,?)",(tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage))
		con.commit()
		cur.close()
		return jsonify({'success': True})

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
			# NEED TO FETCH CORRECT COLOR BY JOINING WITH TRIP - RIGHT NOW, HARDCODED WITH RED
			tempDict = {'firstPointLat': flight['deptLat'], 'firstPointLong': flight['deptLong'], 'secondPointLat': flight['arrLat'], 'secondPointLong': flight['arrLong'], 'color':'red'}
			flights.append(tempDict)
		print('here')

		print(flights)
		# return jsonify({'flights': flights, 'success': 'true'})
		return jsonify({'flights': [{'firstPointLat': 42, 'firstPointLong': 42, 'secondPointLat': 21, 'secondPointLong': 21, 'color':'red'}], 'success': 'true'})
	else: # request method is a POST
		return {}


@app.route('/trips', methods=['GET', 'POST'])
def trips():
	form = TripsForm(request.form)
	if request.method == 'POST' and form.validate():
		uid = form.uid.data
		trip_name = form.trip_name.data
		with sql.connect("app.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			cur.execute("INSERT INTO trip (uid, trip_name) VALUES (?,?)",(uid, trip_name))
			con.commit()
			cur.close()
			flash('You Added A Trip!')
			return redirect('/list')
	return {'trips':[]}

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

@app.route('/update')
def update():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("INSERT INTO user(uid, username, email, password, public) VALUES(1, 'llama', 'llama@gmail.com', 'llamallamallama', 1)")
		cur.execute("INSERT INTO user(uid, username, email, password, public) VALUES(2, 'alpaca', 'alpaca@gmail.com', 'alpacaalpacaalpaca', 1)")
		cur.execute("INSERT INTO trip(tid, uid, trip_name) VALUES(1,1,'llama')")
		cur.execute("INSERT INTO airline(iata, name) VALUES('SQ', 'Singapore Airlines')")
		con.commit()
		cur.close()
	return render_template('home.html')

if __name__ == '__main__':
   app.run(debug = True)
