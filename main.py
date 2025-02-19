from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = "Very_secret_secret_key"

login_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password= "3232",
    database="fcs"
)

cursor = login_db.cursor()


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/myclub")
def myclub():
    if 'user' in session:
        return render_template('my_club.html', user=session['user'][1])
    return render_template('my_club.html', user=None)

@app.route("/matches")
def matches():
    query = "SELECT * FROM matches"
    cursor.execute(query)
    matches = cursor.fetchall()
    return render_template('matches.html', matches=matches)


@app.route("/registerform", methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        flash('Email already exists')
        return redirect(url_for('register', messege='Email already exists'))
    else:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        login_db.commit()
        flash('You have successfully registered')
        return redirect(url_for('login'))
    
@app.route("/login_form", methods=['POST'])
def login_form():
    username = request.form['username']
    # email = request.form['email']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and password == user[2]:
        session["user"] = user
        flash('Successfully logged in!', "success")
        return redirect(url_for("home"))
    else:
        return render_template("login.html", message="Invalid credentials")

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out!', "success")
    return redirect(url_for('home'))

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', user=session['user'][1])
    return render_template('index.html', user=None)





if __name__ == '__main__':
    app.run(debug=True)
