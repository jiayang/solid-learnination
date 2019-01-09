from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def home():
    return render_template('login.html')
