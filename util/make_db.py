import sqlite3

'''Creates the database with tables'''
db = sqlite3.connect("../data/database.db")
c = db.cursor()
#create users
command = "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password_hash TEXT)"
c.execute(command)


db.commit()
db.close()
