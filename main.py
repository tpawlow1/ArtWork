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

@app.get("/")
def index():
    return render_template('index.html')

@app.get("/signup")
def get_Signup():
    return render_template('signup.html')

@app.post("/signup")
def Signup():
    # TODO 


    return render_template('/')

