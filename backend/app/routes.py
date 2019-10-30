from app import app
from flask import render_template
import sqlite3 as sql

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list')
def list():
	with sql.connect("database.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		#cur.execute('CREATE TABLE IF NOT EXISTS users (uid INT, username TEXT, email TEXT, password TEXT, public BOOLEAN)')
		cur.execute("select * from users")
		rows = cur.fetchall()
		cur.close()
	return render_template("list.html",rows = rows)

@app.route('/update')
def update():
	with sql.connect("database.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("INSERT INTO users(uid, username, email, password, public) VALUES(1, 'llama', 'llama@gmail.com', 'llamallamallama', 1)")
		cur.execute("INSERT INTO users(uid, username, email, password, public) VALUES(2, 'alpaca', 'alpaca@gmail.com', 'alpacaalpacaalpaca', 1)")
		con.commit()
		cur.close()
	return render_template('home.html')

if __name__ == '__main__':
   app.run(debug = True)
