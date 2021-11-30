
# Lance Fairbanks
# ljf19a
# 9/29/2021
# The program in this file is the individual work of Lance Fairbanks

import sqlite3

#Connect to the Gainz Database
conn = sqlite3.connect('Gainz.db')
print ("Opened database successfully")

#Create table for login
conn.execute('CREATE TABLE login (username TEXT,firstname TEXT, lastname TEXT, gender TEXT, phone TEXT, address TEXT, email TEXT, password TEXT)')
conn.execute('CREATE TABLE Workouts (userID TEXT, workoutName TEXT, workInterval TEXT, restInterval TEXT, color TEXT, workouts TEXT)')
print ("Tables created successfully")

#Close the Connection
conn.close()
