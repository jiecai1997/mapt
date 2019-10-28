from app import app
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute('CREATE TABLE users (uid INT, username TEXT, email TEXT, password TEXT, public BOOLEAN)')
print "Table created successfully";
conn.close()

if __name__ == '__main__':
	app.run(debug=True)