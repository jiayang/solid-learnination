from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from passlib.hash import md5_crypt
import os

from util import dbcommands as db
from util import msf

app = Flask(__name__)
app.secret_key = os.urandom(32)
LEAGUES = ['nba','nfl','nhl','mlb']

@app.route('/')
def index():
    '''Shows the user the login and register buttons'''
    if "user" in session:
        return redirect(url_for('home'))
    return render_template('landing.html')


@app.route('/login')
def login():
    '''Lets the user log in'''
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/auth', methods = ["POST"])
def auth():
    '''Intermediate to authenticate login by user'''
    if 'user' in session:
        return redirect(url_for('home'))
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
    '''Adding users to the database'''
    if 'user' in session:
        return redirect(url_for('home'))
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
    name=session['user']
    return render_template(
        'home.html',
        name=name,
        favorites=db.get_favorites(name)
        )

@app.route("/<league>", methods=['GET', 'POST'])
def league_page(league):
    '''The pages for the league, which shows the list of teams'''
    if league not in LEAGUES:
        return redirect(url_for('home'))
    return render_template(
        'league.html',
        schedule = msf.get_full_schedule(league),
        teams = msf.all_teams(league),
        league = league
        #get the team names from api
        )


@app.route('/favorite', methods=['POST'])
def favorite():
    if 'data' not in request.form:
        return redirect('/')
    data = request.form['data']
    user = session['user']
    db.add_favorite(user, data)
    print(data)
    return redirect('/home')



@app.route("/<league>/team/<team_name>")
def teams(league,team_name):
    if league not in LEAGUES:
        return redirect(url_for('home'))
    league_games = msf.get_full_schedule(league)
    games = msf.reorder_schedule_by_team(league_games,team_name)
    players = msf.get_all_players_by_team(league,team_name)
    return render_template(
        'teamPage.html',
        league = league.lower(),
        team = team_name.lower(),
        games = games,
        players = players
    )

@app.route("/<league>/game/<game_id>")
def game(league,game_id):
    boxscore = msf.get_boxscore(league,game_id)
    if boxscore == None:
        return render_template(
        'game_not_found.html'
        )
    if league == 'nba':
        return render_template(
        'nba_game_stats.html',
        boxscore = boxscore
        )
    if league =='nhl':
        return render_template(
        'nhl_game_stats.html',
        boxscore = boxscore
        )
    if league == 'mlb':
        return render_template(
        'mlb_game_stats.html',
        boxscore = boxscore
        )
    if league == 'nfl':
        return render_template(
        'nfl_game_stats.html',
        boxscore = boxscore
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
