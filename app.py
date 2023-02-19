from flask import Flask, render_template, request
import mysql.connector
import os


app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password", 
    database= "ArtWork"
)

mysqlcursor = mydb.cursor()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.get("/")
def index():
    return render_template('index.html')

@app.get("/signup")
def get_Signup():
    return render_template('signup.html')

@app.get("/createpost")
def get_createPost():
    return render_template('createPost.html')

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

@app.post('/createpost')
def createPost():
    
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    imageurl = request.form.get('imageurl')
    #imagefile = request.files['imagefile']

    addcom = 'INSERT INTO Posts VALUES (%s, %s, %s, %s)'
    addvals = (title, description, price, imageurl)
    #addcom = 'INSERT INTO Posts VALUES (%s, %s, %s, %s, %s)'
    #addvals = (title, description, price, imagefile.filename, imagefile.read())
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    return render_template('index.html')


if __name__ == "__main__":
    app.run()

