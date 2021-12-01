from app import app, db
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import RegistrationForm, LoginForm, WorkoutForm
from app.models import User, Workouts
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
    form = WorkoutForm()
    if form.validate_on_submit():
        new_workout = Workouts(title = form.title.data, setTime = form.workInterval.data,\
        restTime = form.restInterval.data, workoutsList = form.workoutBlock.data)
        db.session.add(new_workout)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('workout/addWorkout.html', form=form)


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
