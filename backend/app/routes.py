from app import app
from flask import render_template, flash, redirect, url_for, session, request
from app.forms import LoginForm, RegisterForm
import sqlite3 as sql

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('/'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		print(username)
		print(email)
		print(password)
		with sql.connect("app.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			# TODO display page properly if constraint is violated
			n = cur.execute("SELECT MAX(uid) FROM user").fetchone()[0]
			cur.execute("INSERT INTO user (uid, username, email, password, public) VALUES (?,?,?,?,?)",(n+1, username, email, password, 1))
			con.commit()
			cur.close()
			flash('Thanks for registering')
			return redirect('/list')
	return render_template('register.html', title='Register', form=form)

@app.route('/flights/<uid>')
def user_flights(uid):
	with sql.connect("app.db") as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM flights WHERE uid = VALUES(?)"), (uid)
		flightsrows = cur.fetchall()
		cur.close()
	return render_template("list.html",flightsrows = flightsrows)

@app.route('/list')
def list():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("select * from user")
		userrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from trips")
		tripsrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from airlines")
		airlinesrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from airports")
		airportsrows = cur.fetchall()
		cur.close()
		cur = con.cursor()
		cur.execute("select * from flights")
		flightsrows = cur.fetchall()
		cur.close()
	return render_template("list.html",userrows = userrows,tripsrows = tripsrows,
    airlinesrows = airlinesrows, airportsrows = airportsrows, flightsrows = flightsrows)

if __name__ == '__main__':
   app.run(debug = True)
