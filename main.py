from flask import Flask
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password"
)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"