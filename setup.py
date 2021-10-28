#Jason Graham JG19M && Lance Fairbanks LJF19a
#The program in this file is the individual work of Jason Graham and group members


import sqlite3

conn = sqlite3.connect('Gainz.db')
print ("Opened database successfully")

##sets up two tables in the database
conn.execute('CREATE TABLE login (username TEXT,firstname TEXT, lastname TEXT, gender TEXT, phone TEXT, address TEXT, email TEXT, password TEXT)')
conn.execute('CREATE TABLE Workouts (Name TEXT, Type TEXT, Exercises TEXT)')
print ("Login Table created successfully")

conn.close()
