# Jason Graham JG19M && Lance Fairbanks LJF19a && Marcos Sivira && Jared Geiger JDG18
# The program in this file is the individual work of Jason Graham and group members

from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# HTML PAGES
@app.route('/')
def homepage():
    return render_template('index.html')


# login to website
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('workouts'))
    return render_template('login.html', error=error)


@app.route('/hub')
def hub():
    return render_template('hub.html')


# Takes the user to the register html page so they can input their account information
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        try:
            use = request.form['username:']
            fir = request.form['firstname:']
            las = request.form['lastname:']
            gen = request.form['gender:']
            pho = request.form['phone:']
            add = request.form['address:']
            ema = request.form['email:']
            pas = request.form['pass:']

            with sql.connect("Gainz.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO login (username, firstname,lastname,gender,phone,address,email,password) VALUES (?,?,?,?,?,?,?,?)",
                    (use, fir, las, gen, pho, add, ema, pas))
                con.commit()
                print("Account successfully registered.")
        except:
            con.rollback()
            print("error in insert operation")
        finally:
            return redirect(url_for('login'))
            con.close()


@app.route('/workouts')
def workouts():
    return render_template('workouts.html')


@app.route('/addWorkout')
def addWorkout():
    return render_template('addWorkout.html')


@app.route('/editWorkout')
def editWorkout():
    return render_template('editWorkout.html')


@app.route('/completeWorkout')
def completeWorkout():
    return render_template('completeWorkout.html')


# Forms and Lists
@app.route('/addWorkoutForm')
def addWorkoutForm():
    return render_template('workouts.html')


@app.route('/editWorkoutForm')
def editWorkoutForm():
    return render_template('workouts.html')


@app.route('/completeWorkoutList')
def completeWorkoutList():
    return render_template('completeWorkoutModule.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0');
