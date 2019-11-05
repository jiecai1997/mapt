from app import app, db, bcrypt
from flask import render_template, flash, redirect, url_for, session, request
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3 as sql

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		email = form.email.data
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		with sql.connect("app.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			# TODO display page properly if constraint is violated
			n = cur.execute("SELECT MAX(uid) FROM user").fetchone()[0]
			cur.execute("INSERT INTO user (uid, username, email, password, public) VALUES (?,?,?,?,?)",(n+1, username, email, hashed_password, 1))
			con.commit()
			cur.close()
			flash('Thanks for registering')
			return redirect('/list')
	return render_template('register.html', title='Register', form=form)

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

@app.route('/update')
def update():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("INSERT INTO user(uid, username, email, password, public) VALUES(1, 'llama', 'llama@gmail.com', 'llamallamallama', 1)")
		cur.execute("INSERT INTO user(uid, username, email, password, public) VALUES(2, 'alpaca', 'alpaca@gmail.com', 'alpacaalpacaalpaca', 1)")
		cur.execute("INSERT INTO trips(tid, uid, trip_name) VALUES(1,1,'llama')")
		con.commit()
		cur.close()
	return render_template('home.html')

if __name__ == '__main__':
   app.run(debug = True)
