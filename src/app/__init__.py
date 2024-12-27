from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from src.app.secret_key_handler import read_secret_key
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = read_secret_key('src/app/.flask_s_key.dat')

users_db_path = os.path.join(os.path.dirname(__file__), 'users', 'users.db')
users_db_uri = 'sqlite:///{}'.format(users_db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = users_db_uri

inventory_db_uri = os.path.join(os.getcwd(), 'src', 'database', 'inventory.db')
app.config['SQLALCHEMY_BINDS'] = {
    'inventory': f'sqlite:///{inventory_db_uri}' 
}

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