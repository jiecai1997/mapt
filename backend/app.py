from app import app
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

if __name__ == '__main__':
	app.run(debug=True)
