from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password", 
    database= "testdb"
)


mysqlcursor = mydb.cursor()

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/signup")
def Signup():
    return render_template('signup.html')

