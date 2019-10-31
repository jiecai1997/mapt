from app import app
from flask import render_template, flash, redirect
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
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Register requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('/'))
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
	return render_template("list.html",userrows = userrows,tripsrows = tripsrows)

@app.route('/update')
def update():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		#cur.execute("INSERT INTO user(uid, username, email, password, public) VALUES(1, 'llama', 'llama@gmail.com', 'llamallamallama', 1)")
		#cur.execute("INSERT INTO user(uid, username, email, password, public) VALUES(2, 'alpaca', 'alpaca@gmail.com', 'alpacaalpacaalpaca', 1)")
		cur.execute("INSERT INTO trips(tid, uid, trip_name) VALUES(1,1,'llama')")
		con.commit()
		cur.close()
	return render_template('home.html')

if __name__ == '__main__':
   app.run(debug = True)
