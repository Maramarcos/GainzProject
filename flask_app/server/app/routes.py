from app import app, db
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import RegistrationForm, LoginForm, WorkoutForm
from app.models import User
import sqlite3 as sql

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
            workouts = ['       ', 'taco', 'pizza']
            progress = ['       ', 'taco', 'pizza']
            return render_template('base/index.html', workouts = workouts, progress = progress)
    return render_template('base/home.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(name = form.username.data, email = form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user/register.html', form=form)

@app.route('/healthtips')
def healthtips():
    return render_template('info/healthtips.html')

@app.route('/credits')
def credits():
    return render_template('info/credits.html')


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login a new user.'''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash(('Successfully logged in!',"success"))
            return redirect(url_for("index"))
    return render_template('user/login.html', form=form)

# This is for dropdown of workouts

@app.route('/workoutsSelect', methods=['POST'])
def workoutsSelect():
    if request.method == 'POST':
        return render_template('base/index.html')


# This is for dropdown of progress reports

@app.route('/progressSelect', methods=['POST'])
def progressSelect():
    if request.method == 'POST':
        return render_template('base/index.html')


# This is for creating a workout
@app.route('/workout/addWorkout',  methods=['GET', 'POST'])
def addWorkout():
    return render_template('workout/addWorkout.html')


@app.route('/workout/addWorkoutNow',  methods=['GET', 'POST'])
@login_required
def addWorkoutNow():
    if request.method == 'POST':
        try:
            title = request.form['title']
            setTime = request.form['workInterval']
            restTime = request.form['restInterval']
            W1 = request.form['W1']
            W2 = request.form['W2']
            W3 = request.form['W3']
            W4 = request.form['W4']
            W5 = request.form['W5']
            W6 = request.form['W6']
            W7 = request.form['W7']
            W8 = request.form['W8']
            W9 = request.form['W9']
            W10 = request.form['W10']

            with sql.connect("app.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO workouts(title,setTime,RestTime,W1,W2,W3,W4,W5,W6,W7,W8,W9,W10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(title,setTime,restTime,W1,W2,W3,W4,W5,W6,W7,W8,W9,W10) )

                con.commit()
                msg = "Records successfully added!"

        except:
            con.rollback()
            msg = "Error in insertion!"

        finally:
            return render_template('base/index.html')
            con.close()

# This is for creating a report

@app.route('/workout/addReport',  methods=['GET', 'POST'])
@login_required
def addReport():
    '''Create a new workout.'''
    form = WorkoutForm()
    return render_template("workout/addReport.html", form=form)

# This is for running a workout

@app.route('/workout/<workout_title>')
@login_required
def workout(workout_title, methods=['GET']):
    '''Display workout by title.'''
    return ""
