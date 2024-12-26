from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)

db_path = os.path.join(os.path.dirname(__file__), 'users', 'users.db')
print(db_path)
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
users_database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You have to be logged in to access this page.'
login_manager.login_message_category = 'alert-info'

from src.app import routes, users_database

with app.app_context():
    users_database.create_all()