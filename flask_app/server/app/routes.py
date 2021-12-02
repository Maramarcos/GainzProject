from app import app, db
from flask import Flask, render_template, redirect, url_for, flash, request, g
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import RegistrationForm, LoginForm, WorkoutForm, ProgressForm
from app.models import User, Workouts, Progress
import sqlite3 as sql
import sys

# using globals for workout run and registration model Workout and Progression

New = 0

Sets = 0
wList = []
Title = ""
sTime = ""
rTime = ""
Counter = ""


# index route, sets model workout/progression
# Sends to index if authorized, otherwise sends to home
# Dropdowns for workout/progression queried through workouts and progression tables
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
            global New
            if New == 1:
                g.user = current_user.get_id()
                Title = "Quick Pushup Workout"
                SetTime = 30
                RestTime = 10
                WorkoutsList = "Do as many pushups as you can!"

                ex_workout = Workouts(userid = g.user, title = Title, setTime = SetTime,\
                restTime = RestTime, workoutsList = WorkoutsList)
                db.session.add(ex_workout)
                db.session.commit()
                New = 0

                Date = "Welcome to Gainz!"
                Report = "Here you can keep track of your progress like a journal! You know. things like significant gains, or what foods you should start avoiding. Anything! As long as it helps you progress. Good Luck!"

                ex_progress = Progress(userid = g.user, date = Date, report = Report)
                db.session.add(ex_progress)
                db.session.commit()

            g.user = current_user.get_id()
            workouts = []
            for value in db.session.query(Workouts.title).filter(Workouts.userid == g.user):
                workouts.append(value)
            workouts = [i[0] for i in workouts]
            progress = []
            for rep in db.session.query(Progress.date).filter(Progress.userid == g.user):
                progress.append(rep)
            progress = [i[0] for i in progress]
            return render_template('base/index.html', workouts = workouts, progress = progress)
    return render_template('base/home.html')

# Registration generates new user and sends info to user table
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        global New
        New = 1
        new_user = User(name = form.username.data, email = form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('user/register.html', form=form)

# Displays healthtips page
@app.route('/healthtips')
def healthtips():
    return render_template('info/healthtips.html')

# Displays credits page
@app.route('/credits')
def credits():
    return render_template('info/credits.html')

# Displays profile page
@app.route('/profile')
def profile():
    return render_template('info/profile.html')

# Displays feedback page
@app.route('/feedback')
def feedback():
    if request.method == 'POST':
        return render_template('base/index.html')
    return render_template('info/feedback.html')

# Logs out user by unauthenticating and sends back to home
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

# Authorizes user and sends them to index
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
# Submission queries relative workout info and sends to workout start
@app.route('/workoutsSelect', methods=['POST'])
def workoutsSelect():
    if request.method == 'POST':
        global Sets, wList, Title, sTime, rTime, Counter
        title = request.form["workout"]

        g.user = current_user.get_id()
        wList = []

        Title = db.session.query(Workouts.title).filter(Workouts.userid == g.user, Workouts.title == title).one()
        Title = str(Title)
        Title = Title.replace("(\'","")
        Title = Title.replace("\',)","")

        sTime = db.session.query(Workouts.setTime).filter(Workouts.userid == g.user, Workouts.title == title).one()
        sTime = str(sTime)
        sTime = sTime[1:]
        sTime = sTime.replace(",)","")
        sTime = int(sTime)

        rTime = db.session.query(Workouts.restTime).filter(Workouts.userid == g.user, Workouts.title == title).one()
        rTime = str(rTime)
        rTime = rTime[1:]
        rTime = rTime.replace(",)","")
        rTime = int(rTime)

        xList = db.session.query(Workouts.workoutsList).filter(Workouts.userid == g.user, Workouts.title == title).one()

        for x in xList:
            wList.append(x)
        wList = str(wList)
        wList = wList[2:]
        wList = wList[0:-2]

        wList = wList.split("\\r\\n")

        Sets = len(wList)
        Counter = -1

        print(Title,file=sys.stderr)
        print(sTime,file=sys.stderr)
        print(rTime,file=sys.stderr)
        print(wList,file=sys.stderr)
        print(Sets,file=sys.stderr)

        return render_template('workout/running/start.html')
    return render_template('base/index.html')


# This is for dropdown of progress reports
# Submission queries relative progress report info and sends to viewReport
@app.route('/progressSelect', methods=['POST'])
def progressSelect():
    if request.method == 'POST':
        date = request.form["prog"]

        g.user = current_user.get_id()

        Date = db.session.query(Progress.date).filter(Progress.userid == g.user, Progress.date == date).one()
        Date = str(Date)
        Date = Date.replace("(\'","")
        Date = Date.replace("\',)","")

        Report = db.session.query(Progress.report).filter(Progress.userid == g.user, Progress.date == date).one()
        Report = str(Report)
        Report = Report[2:]
        Report = Report[0:-3]


        print(Date,file=sys.stderr)
        print(Report,file=sys.stderr)

        date = Date
        report = Report

        return render_template('workout/viewReport.html', date=date, report=report)
    return render_template('base/index.html')


# This is for creating a workout
@app.route('/workout/addWorkout',  methods=['GET', 'POST'])
def addWorkout():
    form = WorkoutForm()
    g.user = current_user.get_id()

    if form.validate_on_submit():
        new_workout = Workouts(userid = g.user, title = form.title.data, setTime = form.workInterval.data,\
        restTime = form.restInterval.data, workoutsList = form.workoutBlock.data)
        db.session.add(new_workout)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('workout/addWorkout.html', form=form)


# This is for creating a report
@app.route('/workout/addReport',  methods=['GET', 'POST'])
@login_required
def addReport():
    form = ProgressForm()
    g.user = current_user.get_id()

    if form.validate_on_submit():
        new_progress = Progress(userid = g.user, date = form.date.data, report = form.report.data)
        db.session.add(new_progress)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('workout/addReport.html', form=form)

# This is for running a workout
# These are the phases of the process, regulated by counters and sets, and shown with the relative html pages.
@app.route('/workout/start')
def start():
    start = 0
    return render_template("workout/running/start.html", start=start)

@app.route('/workout/exercise')
def exercise():
    global Sets, Counter, sTime, wList
    if Sets == 0:
        return redirect(url_for("complete"))
    Counter+=1
    Sets-=1
    current = wList[Counter]
    setTime = sTime
    return render_template("workout/running/exercise.html", current=current, setTime = setTime)

@app.route('/workout/rest')
def rest():
    global rTime
    if Sets == 0:
        return redirect(url_for("complete"))
    restTime = rTime
    return render_template("workout/running/rest.html", restTime = restTime)

@app.route('/workout/complete')
def complete():
    global Title
    title = Title
    return render_template("workout/running/complete.html", title=title)
