from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = "Very_secret_secret_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
