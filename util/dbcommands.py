#util commands for messing with the database
import sqlite3
DB_FILE ="data/database.db"
#----------------when you want to add data to the database------------------------------
#adds to the users table
def add_user(username,password_hash):
    '''adds users to user table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO users (username,password)VALUES(?,?);"
    c.execute(command,(username,password_hash))
    db.commit()
    db.close()


def get_all_users():
    '''gets all user data into a dict'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command  = "SELECT username,password FROM users;"
    c.execute(command)
    userInfo = c.fetchall()
    db.close()
    dict = {}
    for item in userInfo:
        dict[item[0]] = item[1]
    return dict


def get_user_id(username):
    '''gets user id based on username'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id FROM users WHERE username = ?;"
    c.execute(command,(username,))
    user_id = c.fetchall()
    db.close()
    return user_id[0][0]


def get_username(id):
    '''get username based on id'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT username FROM users WHERE id = ?;"
    c.execute(command,(id,))
    name = c.fetchall()
    db.close()
    return name[0][0]



def add_favorite(username, data):
    '''adds favorites to favorite table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = 'INSERT INTO favorites VALUES(?, ?)'
    c.execute(command, (username, data))
    db.commit()
    db.close()

def add_balance(username):
    '''adds balance to balance table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = 'INSERT INTO balance VALUES(?, ?)'
    c.execute(command, (username, 1000))
    db.commit()
    db.close()

def remove_favorite(username, data):
    '''removes favorite from the favorite table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = 'DELETE FROM favorites WHERE username = ? AND favorites = ?'
    c.execute(command, (username, data))
    db.commit()
    db.close()


def get_favorites(username):
    '''gets favorites from the favorite table based on username'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command =  "SELECT * FROM favorites WHERE username=?"
    c.execute(command, (username,))
    results = c.fetchall()
    favorites = [i[1].split('-----') for i in results]
    db.close()
    return favorites

def get_balance(username):
    '''gets balance from balance table based on username'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command =  "SELECT * FROM balance WHERE username=?"
    c.execute(command, (username,))
    results = c.fetchall()
    db.close()
    return results[0][1]

def add_bets(username, val, league, Gid, team):
    '''add bets to the bets table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = 'INSERT INTO bets VALUES(?, ?, ?, ?, ?)'
    c.execute(command, (username, val, league, Gid, team))
    print(team)
    db.commit()
    db.close()

def get_bets(username):
    '''get bets from bets table based on username'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command =  "SELECT * FROM bets WHERE username=?"
    c.execute(command, (username,))
    results = c.fetchall()
    db.close()
    return results
# [('joe', 300, 'nfl', 45266, 'cleveland-cavaliers'), ('joe', 300, 'nfl', 45266, 'cavaliers'), ('joe', 308, 'nfl', 452, 'caiers')]

def update_balance(username, New_val):
    '''add to balance table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "UPDATE balance SET money=? WHERE username=?"
    c.execute(command, (New_val, username))
    db.commit()
    db.close()

def remove_bet(username, game_id):
    '''remove bet from bets table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = 'DELETE FROM bets WHERE username = ? AND gameID = ?'
    c.execute(command, (username, game_id))
    db.commit()
    db.close()

# MAKE TABLES AND DATABASE IF THEY DONT EXIST
db = sqlite3.connect(DB_FILE)
c = db.cursor()
commands = []
commands += ["CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)"]
commands += ["CREATE TABLE IF NOT EXISTS favorites(username TEXT, favorites TEXT)"]
commands += ["CREATE TABLE IF NOT EXISTS balance(username TEXT, money INTEGER)"]
commands += ["CREATE TABLE IF NOT EXISTS bets(username TEXT, money INTEGER, league TEXT, gameID INTEGER, team TEXT)"]
for command in commands:
    c.execute(command)
db.commit()
c.close()
