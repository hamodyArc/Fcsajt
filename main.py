from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
import os
from flask import jsonify
import random

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
        return render_template('my_club.html', user=session['user'])
    return render_template('login.html', user=None)

@app.route("/matches")
def matches():
    query = "SELECT * FROM matches;"
    cursor.execute(query)
    teams = cursor.fetchall()
    if 'user' in session:
        return render_template('matches.html', teams=teams, user=session['user'])
    return render_template('matches.html', teams=teams, user=None)


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
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
                       (username, password, email))
        login_db.commit()
        flash('You have successfully registered')
        return redirect(url_for('login'))
    
@app.route("/login_form", methods=['POST'])
def login_form():
    username = request.form['username']
    # email = request.form['email']
    password = request.form['password']
    query = """
        SELECT users.*, teams.team_value
        FROM users
        LEFT JOIN teams ON users.username = teams.owner
        WHERE users.username = %s
    """
    cursor.execute(query, (username,))
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
        return render_template('index.html', user=session['user'])
    return render_template('index.html', user=None)


@app.route('/save_players', methods=['POST'])
def save_player():
    data = request.json
    players = data.get('players', [])
    
    player1 = players[0]
    player2 = players[1]
    player3 = players[2]

    player1_name = player1.get('name')
    player2_name = player2.get('name')
    player3_name = player3.get('name')

    player1_id = int(player1.get('id') or 0)
    player2_id = int(player2.get('id') or 0)
    player3_id = int(player3.get('id') or 0)

    total_team_value = player1_id + player2_id + player3_id
    owner = session['user'][1]
    cursor.execute("INSERT INTO userplayers (owner, player1, player2, player3) VALUES (%s ,%s ,%s, %s)", 
                   (owner, player1_name, player2_name, player3_name))
    cursor.execute("INSERT INTO teams (owner, team_value) VALUES (%s, %s)", 
                   (owner, total_team_value))

############################################################################
    query = "SELECT * FROM teams;"
    cursor.execute(query)
    instance_one = cursor.fetchall() 
    match_time = datetime.now()

    teams2 = random.choice(instance_one)
    
    cursor.execute("INSERT INTO matches (team1_name,team1_value,team2_name,team2_value, datee) VALUES (%s, %s, %s, %s, %s)", 
                   (owner, total_team_value, teams2[1], teams2[2], match_time))
#############################################################################
    login_db.commit()

    return jsonify({"message": "Player saved successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
