from flask import Flask
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
def test():
    query = 'SELECT Message FROM testtable'
    mysqlcursor.execute(query)
    result = mysqlcursor.fetchall()
    message = '<p>' + str(result[0]) + '</p>'
    return message