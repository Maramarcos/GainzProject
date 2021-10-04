#Jason Graham JG19M
#The program in this file is the individual work of Jason Graham and group members


import sqlite3

conn = sqlite3.connect('reviewData.db')
print ("Opened database successfully")

##sets up two tables in the database
conn.execute('CREATE TABLE login (Username TEXT, Name TEXT)')
print ("Login Table created successfully")

conn.close()
