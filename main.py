from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import random

app = Flask(__name__)
app.secret_key = "Very_secret_secret_key"

main = mysql.connector.connect(
    host="localhost",
    user="root",
    password= "3232",
    database="fcs2"
)

cursor = main.cursor()

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/myclub")
def myclub():
    user_id = session['user'][0]
    query = """
        SELECT userplayers.player_id as id, players.player_name, userss.user_id
        FROM userss
        INNER JOIN userplayers
        ON userss.user_id = userplayers.user_id
        INNER JOIN players
        ON userplayers.player_id = players.player_id
        WHERE userss.user_id = %s;
    """
    cursor.execute(query, (user_id,))

    clubs = cursor.fetchall()
    print("clubs", clubs)   
    if 'user' in session:
        return render_template('my_club.html', user=session['user'], clubs=clubs)
    return render_template('login.html', user=None)

@app.route('/remove_player', methods=['POST'])
def remove_player():
    player_id = request.json.get('id')
    user_id = session['user'][0]
    print("user_id", user_id)
    print("player_id", player_id)
    try:
        cursor.execute("DELETE FROM userplayers WHERE player_id = %s AND user_id = %s", (player_id, user_id))
        main.commit()
        return jsonify({"message": "Player removed successfully!"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "An error occurred"}), 500


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

    cursor.execute("SELECT * FROM userss WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        flash('Email already exists')
        return redirect(url_for('register', messege='Email already exists'))
    else:
        cursor.execute("INSERT INTO userss (username, password, email) VALUES (%s, %s, %s)", 
                       (username, password, email))
        main.commit()
        flash('You have successfully registered')
        return redirect(url_for('login'))
    
@app.route("/login_form", methods=['POST'])
def login_form():
    username = request.form['username']
    password = request.form['password']
    cursor.execute("SELECT * FROM userss WHERE username = %s", (username,))
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
    if 'user' not in session:
        return jsonify({"message": "User not logged in"}), 401

    data = request.json
    user_id = session['user'][0] 
    player_id = int(data.get('id'))

    try:
        cursor.execute("SELECT player_id FROM players WHERE player_id = %s", (player_id,))
        player_data = cursor.fetchone()
        if not player_data:
            return jsonify({"message": "Player not found"}), 404

        cursor.execute("SELECT * FROM userplayers WHERE user_id = %s AND player_id = %s", (user_id, player_id))
        if cursor.fetchone():
            return jsonify({"message": "Player already added"}), 400

        cursor.execute("SELECT COUNT(*) FROM userplayers WHERE user_id = %s", (user_id,))
        userplayers_count = cursor.fetchone()[0]

        if userplayers_count < 3:
            cursor.execute("INSERT INTO userplayers (user_id, player_id) VALUES (%s, %s)", (user_id, player_id))
            main.commit()
            return jsonify({"message": "Player saved successfully!"}), 201

        elif userplayers_count == 3:
            cursor.execute("SELECT COUNT(*) FROM matches WHERE team1_id = %s", (user_id,))
            if cursor.fetchone()[0] > 0:
                return jsonify({"message": "You can only save 1 match"}), 400

            cursor.execute("""
                SELECT userss.username, SUM(players.player_rating)
                FROM userplayers
                JOIN players ON userplayers.player_id = players.player_id
                JOIN userss ON userplayers.user_id = userss.user_id
                WHERE userplayers.user_id = %s
                GROUP BY userss.username
            """, (user_id,))
            team1_result = cursor.fetchone()
            if not team1_result:
                return jsonify({"message": "Unable to calculate team rating"}), 500

            team1_name, team1_value = team1_result

            cursor.execute("SELECT user_id FROM userss WHERE user_id != %s ORDER BY RAND() LIMIT 1", (user_id,))
            opponent = cursor.fetchone()
            if not opponent:
                return jsonify({"message": "No opponent available"}), 500

            team2_id = opponent[0]
            cursor.execute("""
                SELECT userss.username, SUM(players.player_rating)
                FROM userplayers
                JOIN players ON userplayers.player_id = players.player_id
                JOIN userss ON userplayers.user_id = userss.user_id
                WHERE userplayers.user_id = %s
                GROUP BY userss.username
            """, (team2_id,))
            team2_result = cursor.fetchone()
            if not team2_result:
                return jsonify({"message": "Opponent has no players"}), 500

            team2_name, team2_value = team2_result

            cursor.execute("""
                INSERT INTO matches (team1_id, team1_rating, team2_id, team2_rating, time_start)
                VALUES (%s, %s, %s, %s, NOW())
            """, (team1_name, team1_value, team2_name, team2_value))

            main.commit()
            return jsonify({"message": "Match saved!"}), 201

        else:
            return jsonify({"message": "You can only have 3 players"}), 400

    except Exception as e:
        print("Error:", str(e))
        main.rollback()
        return jsonify({"message": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)
