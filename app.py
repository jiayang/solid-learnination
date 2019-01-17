from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from passlib.hash import md5_crypt
import os

from util import dbcommands as db
from util import msf
from util import favorites as fav

app = Flask(__name__)
app.secret_key = os.urandom(32)
LEAGUES = ['nba','nfl','nhl','mlb']

@app.route('/')
def index():
    '''Shows the user the login and register buttons'''
    if "user" in session:
        return redirect(url_for('home'))
    return render_template('landing.html', background='https://www.lboro.ac.uk/media/wwwlboroacuk/external/content/research/sti/slide1.png',)


@app.route('/login')
def login():
    '''Lets the user log in'''
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html', background='http://www.tsul.uz/files/obyavleniya/01.09.2018/sss960.jpg',)

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
            session['balance'] = db.get_balance(username_input)
            check_bet_updates(session['user'])

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
            db.add_balance(r_username)
            session['balance'] = db.get_balance(r_username)
            return redirect(url_for("home"))
    return render_template('register.html', background='http://www.tsul.uz/files/obyavleniya/01.09.2018/sss960.jpg',)

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
    favorites = db.get_favorites(name)
    favorites = fav.organize_by_league(favorites)
    return render_template(
        'home.html',
        name=name,
        favorites=favorites,
        balance = session['balance']
        )

@app.route("/<league>", methods=['GET', 'POST'])
def league_page(league):
    '''The pages for the league, which shows the list of teams'''
    if league not in LEAGUES:
        return redirect(url_for('home'))
    if 'user' not in session:
        return redirect(url_for('login'))
    favorites = db.get_favorites(session['user'])
    favorites = fav.organize_by_team(favorites)
    return render_template(
        'league.html',
        schedule = msf.get_full_schedule(league),
        teams = msf.all_teams(league),
        league = league,
        favorites = favorites,
        name = session['user'],
        balance = session['balance']
        )


@app.route('/favorite', methods=['POST'])
def favorite():
    if 'favdata' not in request.form:
        return redirect('/')
    data = request.form['favdata']
    user = session['user']
    db.add_favorite(user, data)
    return redirect('/home')

@app.route('/unfavorite', methods=['POST'])
def unfavorite():
    if 'unfav' not in request.form:
        return redirect('/')
    data = request.form['unfav']
    user = session['user']
    db.remove_favorite(user,data)
    return redirect('/home')

@app.route("/<league>/team/<team_name>")
def teams(league,team_name):
    if 'user' not in session:
        return redirect(url_for('login'))
    if league.lower() not in LEAGUES:
        return redirect(url_for('home'))
    league_games = msf.get_full_schedule(league)
    games = msf.reorder_schedule_by_team(league_games,team_name)
    players = msf.get_all_players_by_team(league,team_name)
    played_games = msf.get_played_games_win_loss(league,team_name)

    users_bets = db.get_bets(session['user'])
    Gid = []
    for bet in users_bets:
        Gid.append(str(bet[3]))
    return render_template(
        'teamPage.html',
        league = league.lower(),
        team = team_name,
        games = games,
        players = players,
        played_games = played_games,
        name = session['user'],
        balance = session['balance'],
        bet_gid = Gid
    )

@app.route("/<league>/game/<game_id>")
def game(league,game_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    boxscore = msf.get_boxscore(league,game_id)
    name = session['user']
    bal = session['balance']
    if boxscore == None:
        return render_template(
        'game_not_found.html',
        name = name,
        balance = bal
        )
    if league == 'nba':
        return render_template(
        'nba_game_stats.html',
        boxscore = boxscore,
        name = name,
        balance = bal
        )
    if league =='nhl':
        return render_template(
        'nhl_game_stats.html',
        boxscore = boxscore,
        name = name,
        balance = bal
        )
    if league == 'mlb':
        return render_template(
        'mlb_game_stats.html',
        boxscore = boxscore,
        name = name,
        balance = bal
        )
    if league == 'nfl':
        return render_template(
        'nfl_game_stats.html',
        boxscore = boxscore,
        name = name,
        balance = bal
        )

@app.route("/Make_bets/<league>/<game_id>/<home>/<away>")
def Makebets(league, game_id, home, away):
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('makeBets.html', league=league, game_id = game_id, homeTeam = home, awayTeam= away,name = session['user'], balance = session['balance'])

@app.route("/Auth_bets/<league>/<game_id>/<home>/<away>")
def Authbets(league, game_id, home, away):
    if 'user' not in session:
        return redirect(url_for('login'))
    user_bal = session['balance']
    team = request.args.get("chosen_team")
    if team == None:
        flash("Choose a Team!")
        return render_template('makeBets.html', league=league, game_id = game_id, homeTeam = home, awayTeam= away,name = session['user'], balance = session['balance'])
    try:
        amount = int(request.args.get("value"))
    except:
        flash("Enter a monetary value!")
        return render_template('makeBets.html', league=league, game_id = game_id, homeTeam = home, awayTeam= away,name = session['user'], balance = session['balance'])
    if amount > user_bal:
        flash("The amount you bet is higher than your current balance... Try again!")
        return render_template('makeBets.html', league=league, game_id = game_id, homeTeam = home, awayTeam= away,name = session['user'], balance = session['balance'])
    elif amount < 100:
        flash("The amount you bet is too little... Try again!")
        return render_template('makeBets.html', league=league, game_id = game_id, homeTeam = home, awayTeam= away,name = session['user'], balance = session['balance'])
    else:
        db.add_bets(session['user'], amount, league, int(game_id), team)
        val = user_bal - amount
        print(val)
        db.update_balance(session['user'], val)
        session['balance'] = val
        all_bets = db.get_bets(session['user'])
        return redirect(url_for("bet_already"))


@app.route("/your_bets")
def bet_already():
    if 'user' not in session:
        return redirect(url_for('login'))
    all_bets = db.get_bets(session['user'])
    return render_template('bets.html', bets_made = all_bets, name =session['user'], balance =session['balance'] )

#regular funciton
def check_bet_updates(username_input):
    users_bets = db.get_bets(username_input)
    for bet in users_bets:
        game_id = str(bet[3])
        league = bet[2]
        team_name = bet[4]
        played_games = msf.get_played_games_win_loss(league,team_name)
        if game_id in played_games:
            db.remove_bet(session['user'],game_id)
            game_info = played_games[game_id]
            #Won
            if game_info['stats']['Wins']['#text'] == '1':
                #add double
                #flash
                cur_bal = session['balance']
                to_add = bets[1] * 2
                cur_bal += to_add
                session['balance'] = cur_bal
                db.update_balance(session['user'],cur_bal)
            else:
                #flash messages
                pass

if __name__ == "__main__":
    app.debug = True
    app.run()
