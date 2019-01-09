from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def index():
    if "user" in session:
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route("/login",methods=["GET","POST"])
def login():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #checks if the username exists
        if(dbtools.user_exists(c,username)):
            #checks username and password
            if(dbtools.check_user(c,username,password)):
                # user is added to session and redirected
                session["user"] = username
                return redirect(url_for('home'))
            else:
                #wrong password
                error="wrong password"
        else:
            #case for wrong username
            error="wrong username"
    #checks if the user is logged in already and tries to access the page
    if "user" in session:
        #flashes an error and redirects to home
        flash("You are already logged in.")
        return redirect(url_for('home'))
    #displays the error the user faced when logging in
    flash(error)
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    '''This function lets the user register'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #checks if the username already exists
        if(dbtools.user_exists(c,username)):
            error="the username you inputted already exists!"
        else:
            #fetching most recently added id
            forID = c.execute("SELECT userid FROM users ORDER BY userid DESC LIMIT 1")
            id = forID.fetchone()[0]
            #adds user to database
            dbtools.add_user(c,id+1,username,password)
            #adds user to session
            session["user"] = username
            db.commit()
            db.close()
            #redirects user to home
            return redirect(url_for('home'))
    #checks if the user is logged in already and tries to access the page
    if "user" in session:
        #flashes an error if they try to do so then redirects to home
        flash("You tried to access the register page while logged in! If you wish to create a new account, log out first!")
        return redirect(url_for('home'))
    #displays the error the user faced when registering an account
    flash(error)
return render_template("register.html")


@app.route("/logout")
def logout():
    #checks if the user is not logged in
    if "user" not in session:
        #flashes the error messsage below if they are not logged in
        flash("You tried to log out without being logged in.")
        return redirect(url_for('home'))
    #removes the user from the session
    session.pop("user")
    #redirects back to home
    return redirect(url_for('home'))


@app.route("/home")
def home():
    #checks if the user is not logged in
    if "user" not in session:
        #flashes error
        flash("You're not logged in")
        return redirect(url_for('home'))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #gets the userid of the user in session
    userID = c.execute("SELECT userid FROM users WHERE username = ?",(session["user"]))
    return render_template("userHome.html",username = session["user"])


if __name__ == "__main__":
    app.debug = True
app.run()
