from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password", 
    database= "ArtWork"
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
    # pull information from form ids
    email = request.form.get('usermail')
    username = request.form.get('name')
    userpass1 = request.form.get('pass1')
    userpass2 = request.form.get('pass2')
    # verify passwords match
    if userpass1 != userpass2: 
        return render_template('index.html') # placeholder bounce back if no match
    # if all good, send to user table in database
    addcom = 'INSERT INTO Users VALUES (%s, %s, %s)'
    addvals = (username, email, userpass1)

    mysqlcursor.execute(addcom, addvals)

    mydb.commit()

    return render_template('index.html') # send user back to homepage or sign in


if __name__ == "__main__":
    app.run()

