from src.app import users_database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_usuario):
    return User.query.get(int(id_usuario))


class User(users_database.Model, UserMixin):
    id = users_database.Column(users_database.Integer, primary_key=True)
    username = users_database.Column(users_database.String, nullable=False, unique=True)
    email = users_database.Column(users_database.String, nullable=False, unique=True)
    password = users_database.Column(users_database.String, nullable=False)