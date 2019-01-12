from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from passlib.hash import md5_crypt
import os

from util import dbcommands as db
from util import msf

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def index():
    if "user" in session:
        return redirect(url_for('home'))
    return render_template('landing.html')


@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/auth', methods = ["POST"])
def auth():
    if 'user' in session:
        return redirect(url_for('home'))
    '''Intermediate to authenticate login by user'''
    # # # Authenticate
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    all_usernames = db.get_all_users()
    if username_input in all_usernames:
        # If the hashes match
        if md5_crypt.verify(password_input, all_usernames[username_input]):
            # Log them in
            session['user'] = username_input
            return redirect(url_for("home"))
        # Failed password and username match
        else:
            flash("Invalid password")
    else:
        # Username doesnt exist
        flash("Invalid username")
    return redirect(url_for("login"))

@app.route('/register', methods = ["GET", "POST"])
def register():
    if 'user' in session:
        return redirect(url_for('home'))
    '''Adding users to the database'''
    if request.form.get("reg_username") != None:
        r_username = request.form.get("reg_username")
        r_password = request.form.get("reg_password")
        check_pass = request.form.get("reg_confirm")
        if r_username in db.get_all_users():
            flash("Username taken")
        elif r_password != check_pass:
            flash("Passwords do not match!")
        elif r_password.count(' ') != 0:
            flash("Password can not contain spaces")
        elif not r_username.isalnum():
            flash("Username should be alphanumeric")
        else:
            session['user'] = r_username
            db.add_user(r_username, md5_crypt.encrypt(r_password))
            return redirect(url_for("home"))
    return render_template('register.html')

@app.route('/logout', methods = ['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'))

@app.route("/home")
def home():
    #checks if the user is not logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'home.html',
        name=session['user'],
        favorites=0#util.favorites.get_favorites(name)
        )

@app.route("/nba", methods=['GET', 'POST'])
def nba():
    return render_template(
        'league.html',
        schedule = msf.get_full_schedule('nba'),
        teams = msf.all_teams('nba'),
        league = 'nba'
        #get the team names from api
        )

@app.route("/nba/<team_name>")
def nba_team(team_name):
    return render_template(
        'teamPage.html',
        team = team_name.lower(),
        games = msf.reorder_schedule_by_team(msf.get_full_schedule('nba'),team_name)
    )

@app.route("/nfl", methods=['GET', 'POST'])
def nfl():
    return render_template(
        'league.html',
        schedule = msf.get_full_schedule('nfl'),
        teams = msf.all_teams('nfl'),
        league = 'nfl'
        #get the team names from api
        )

@app.route("/nhl", methods=['GET', 'POST'])
def nhl():
    return render_template(
        'league.html',
        schedule = msf.get_full_schedule('nhl'),
        teams = msf.all_teams('nhl'),
        league = 'nhl'
        #get the team names from api
        )

@app.route("/mlb", methods=['GET', 'POST'])
def mlb():
    return render_template(
        'league.html',
        schedule = msf.get_full_schedule('mlb'),
        teams = msf.all_teams('mlb'),
        league = 'mlb'
        #get the team names from api
        )


@app.route("/team", methods=['GET', 'POST'])
def team():
    return render_template(
        'teamPage.html',
        #get teams info and stats etc from api
        )

@app.route("/bets")
def bets():
    return render_template(
        'bets.html',
        )

@app.route("/test")
def wot():
    return render_template(
        'nba_game_stats.html'
    )


if __name__ == "__main__":
    app.debug = True
app.run()
