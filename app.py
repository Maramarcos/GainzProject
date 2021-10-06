#Jason Graham JG19M && Lance Fairbanks LJF19a
#The program in this file is the individual work of Jason Graham and group members

from flask import Flask, render_template, request
import sqlite3 as sql
from datetime import datetime
app = Flask(__name__)

#login
@app.route('/')
def home():
	return render_template('login.html')

#register for app
@app.route('/register',methods = ['POST', 'GET'])
def register():
	if request.method == 'POST':
		try:
			usr = request.form['Username:']
			nam = request.form['Name:']
			
			with sql.connect("loginData.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO login (Username,Name) VALUES (?,?)",(usr,nam))
				con.commit()
				print("Reviews successfully added")
		except:
			con.rollback()
			print("error in insert operation")
		finally:
			return render_template("home.html")
			con.close()
	
#login to website
@app.route('/login')
def login():
	con = sql.connect("loginData.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute()
	rows = cur.fetchmany(10);
	return render_template("home.html",rows = rows)
	

 #Go to workouts
@app.route('/workouts')
def workouts():
	return render_template('workouts.html')
    
 #Create a workout
@app.route('/addWorkout')
def addWorkout():
	return render_template('addWorkout.html')

    
    
if __name__ == '__main__':
	app.run(host='0.0.0.0');
