from src.app import app
import os


def run_flask_app():
    os.system("gunicorn -w 1 -b 127.0.0.1:5000 --reload siteficha:app")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)