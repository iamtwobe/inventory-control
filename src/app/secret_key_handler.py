import os

def create_secret_key(file_path):
    with open(file_path, 'wb') as f:
        f.write(os.urandom(64))

def read_secret_key(file_path=None):
    if not file_path:
        file_path = 'src/app/.flask_s_key.dat'
    if not os.path.exists(file_path):
        create_secret_key(file_path)
    with open(file_path, 'rb') as f:
        return f.read()