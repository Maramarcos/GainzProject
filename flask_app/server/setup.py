import sqlite3

conn = sqlite3.connect('app.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE Reviews (Username TEXT, Restaurant TEXT, ReviewTime TEXT, Rating REAL, Review TEXT)')
conn.execute('CREATE TABLE Ratings (Restaurant TEXT, Food REAL, Service REAL, Ambience REAL, Price REAL, Overall REAL)')

print ("Tables created successfully")

conn.close()
