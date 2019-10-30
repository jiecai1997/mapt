from flask import Flask
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLALchemy(app)
migarte = Migrate(app,db)


from app import routes, models
