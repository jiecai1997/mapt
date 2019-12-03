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
		return jsonify({'success': True})

@app.route('/trips/add', methods=['POST'])
def addtrip_user():
	json = request.get_json()

	uid = json['uid']
	trip_name = json['trip_name']
	color = json['color']

	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("INSERT INTO trip (uid, trip_name,color) VALUES (?,?,?)",(uid, trip_name,color))
		con.commit()
		cur.close()
		return jsonify({'success': True})

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			session['logged_in'] = True
			return redirect(url_for('home'))
		else:
			error = 'Invalid username or password'
	return render_template('login.html', title='Login', form=form, error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		email = form.email.data
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		print(username)
		print(email)
		with sql.connect("app.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			# TODO display page properly if constraint is violated
			cur.execute("INSERT INTO user (username, email, password, public) VALUES (?,?,?,?)",(username, email, hashed_password, 1))
			con.commit()
			cur.close()
			flash('Thanks for registering')
			return redirect('/list')
	return render_template('register.html', title='Register', form=form)

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
