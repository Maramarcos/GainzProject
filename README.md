# GainzProject
A Python application to help anyone get gains

Steps to run Gainz app:

python3 -m venv flask/
cd flask
source bin/activate (setup virtual environment)
pip install Flask (install all modules)
pip install Flask-Login==0.3.2
pip install sqlalchemy
pip install Flask-Migrate
pip install flask-WTF
pip install email-validator
cd GainzProject-main/flask_app/server
sh setup.sh (database update)
FLASK_APP=server.py
flask run (runs app)

*All modules must be downloaded inside the virtual enviroment
