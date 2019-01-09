import sqlite3

'''Creates the database with tables'''
db = sqlite3.connect("../data/database.db")
c = db.cursor()
#create users
command = "CREATE TABLE users(username TEXT ,password TEXT)"
c.execute(command)


db.commit()
db.close()
