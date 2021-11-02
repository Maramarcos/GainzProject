#Jason Graham JG19M && Lance Fairbanks LJF19a && Marcos Sivira
#The program in this file is the individual work of Jason Graham and group members

from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

# HTML PAGES
@app.route('/')
def homepage():
    return render_template('index.html')

#login to website
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('workouts.html')
    return render_template('login.html', error=error)

@app.route('/hub')
def hub():
    return render_template('hub.html')

#Takes the user to the register html page so they can input their account information
@app.route('/register')
def register():
	return render_template('register.html')

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

#Takes the user to the register html page so they can input their account information
@app.route('/registration',methods = ['POST', 'GET'])
def registeration():
	if request.method == 'POST':
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
				cur.execute("INSERT INTO login (username, firstname,lastname,gender,phone,address,email,password) VALUES (?,?,?,?,?,?,?,?)",(use,fir,las,gen,pho,add,ema,pas))
				con.commit()
				print("Reviews successfully added")
		except:
			con.rollback()
			print("error in insert operation")
		finally:
			return render_template("login.html")
			con.close()

if __name__ == '__main__':
	app.run(host='0.0.0.0');
