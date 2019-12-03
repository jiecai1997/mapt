from app import app, bcrypt
from flask import render_template, flash, redirect, url_for, session, request
from app.forms import LoginForm, RegisterForm, FlightsForm, TripsForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3 as sql
from flask import jsonify

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

		return jsonify({'success': 'true'})

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
			return jsonify({'success': 'false'})

		db_username = urow[0]
		db_email = urow[1]
		db_password = urow[2]

		# success - user exists
		if input_email == db_email and input_password == db_password:
			session_token = username+str(randInt(0, 1000))
			cur.execute("UPDATE user SET session = (?) WHERE email = (?)", [session_token, input_email])
			return jsonify({
					'success': 'true',
					'userid': db_username,
					'sessionToken': session_token
				})

		# fail - wrong password for user
		else:
			return jsonify({'success': 'false'})

		cur.commit()
		cur.close()


@app.route('/user/addtrip', methods=['POST'])
def addtrip_user():
	json = request.get_json()

	uid = json['uid']
	trip_name = json['trip_name']

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("INSERT INTO trip (uid, trip_name) VALUES (?,?)",(uid, trip_name))
		con.commit()
		cur.close()
		return jsonify({'success': True})

@app.route('/')
def home():
    return render_template('home.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


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




@app.route('/manual', methods=['GET', 'POST'])
def manual():
	form = FlightsForm(request.form)
	if request.method == 'POST' and form.validate():
		tid = form.tid.data
		airline_iata = form.airline_iata.data
		flight_num = form.flight_num.data
		depart_iata = form.depart_iata.data
		arrival_iata = form.arrival_iata.data
		depart_datetime = form.depart_datetime.data
		arrival_datetime = form.arrival_datetime.data
		duration = form.duration.data
		mileage = form.mileage.data
		with sql.connect("app.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			cur.execute("INSERT INTO flight (tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage) VALUES (?,?,?,?,?,?,?,?,?)",(tid, airline_iata, flight_num, depart_iata, arrival_iata, depart_datetime, arrival_datetime, duration, mileage))
			con.commit()
			cur.close()
			flash('You Added A Flight!')
			return redirect('/list')
	return render_template('flights.html', title="Add a Flight", form=FlightsForm())

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
	return render_template('trips.html', title="Add a Trip", form=TripsForm())

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
