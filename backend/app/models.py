from app import db

class User(db.Model):
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(20), unique=True, nullable=False)
	public = db.Column(db.Boolean(), nullable=False)

	def __repr__(self):
		return '<User {}>'.format(self.username)
    
