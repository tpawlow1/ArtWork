from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os
import uuid


app = Flask(__name__)
app.secret_key = 'key'

UPLOAD_FOLDER = os.getcwd() + '/static/images'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ArtWork"
)

mysqlcursor = mydb.cursor()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getposts():
    user = session['user']
    # sending all post entries to index to appear
    mysqlcursor.execute(f"SELECT * FROM Posts WHERE user='{user}'")
    data = mysqlcursor.fetchall()

    return data


# get index
@app.get("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        try:
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            mysqlcursor.execute(query, (username, password))
            confirm = mysqlcursor.fetchone()

            if confirm != None:
                session['user'] = username
                return redirect('/profile')
            else:
                return render_template('login.html', message='Invalid login credentials. Please try again.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return render_template('login.html', message='Database error. Please try again later.')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return render_template('index.html')

# get user signup page


@app.get("/signup")
def get_Signup():
    return render_template('signup.html')

# post user info and create user


@app.post("/signup")
def Signup():
    # pull information from form ids
    email = request.form.get('usermail')
    username = request.form.get('name')
    userpass1 = request.form.get('pass1')
    userpass2 = request.form.get('pass2')
    # verify passwords match
    if userpass1 != userpass2:
        # placeholder bounce back if no match
        return render_template('index.html')
    # if all good, send to user table in database
    addcom = 'INSERT INTO Users VALUES (%s, %s, %s, %s, %s)'
    addvals = (username, email, userpass1, '', 'default:profilepic.jpg')
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()
    # sets user's username to user for the session
    session['user'] = username

    # send user to homepage
    return redirect(url_for("homepage"))

# homepage specific to the user that's logged in


@app.get("/homepage")
def homepage():
    user = session['user']
    data = getposts()
    print(len(data))
    return render_template("homepage.html", post=data, user=user)


@app.get("/profile")
def profilePage():
    user = session['user']
    mysqlcursor.execute(f"SELECT * FROM Users WHERE username = '{user}'")
    data = mysqlcursor.fetchall()
    return render_template("profilePage.html", data=data)


@app.post("/profile")
def editProfile():
    user = session['user']
    username = request.form.get('username')
    print(username)
    email = request.form.get('email')
    password = request.form.get('password')
    bio = request.form.get('bio')

    command = f"UPDATE Users SET username='{username}', email='{email}', password='{password}', bio='{bio}' WHERE username = '{user}';"
    mysqlcursor.execute(command)
    mydb.commit()
    command2 = f"UPDATE Posts SET user='{username}' WHERE user='{user}'"
    mysqlcursor.execute(command2)
    mydb.commit()
    session.pop('user', None)
    session['user'] = username
    return redirect("/profile")


# edits profile pic in database
@app.post("/profile/pic")
def editProfilePic():
    user = session['user']

    # pull file from form, get path
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        return redirect('/profile')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    if file:
        file.save(filepath)
    command = f"UPDATE Users SET profilePicPath='{file.filename}' WHERE username='{user}'"
    mysqlcursor.execute(command)
    mydb.commit()
    return redirect("/profile")


# get create post form
@app.get("/createpost")
def get_createPost():
    return render_template('createPost.html')

# upload post information and create post


@app.post('/createpost')
def createPost():
    user = session['user']
    # generate unique id
    postid = str(uuid.uuid4())

    # pull from post
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    # pull file from form, get path
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        return redirect('index.html')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    if file:
        file.save(filepath)

    # add to db
    addcom = 'INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s)'
    addvals = (postid, title, description, price, file.filename, user)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    return redirect('/homepage')


# get post update form
@app.get("/edit/<id>")
def getEditPost(id):
    mysqlcursor.execute("SELECT * FROM Posts WHERE id = '" + str(id) + "'")
    data = mysqlcursor.fetchall()[0]

    # pass with data from specific post
    return render_template('editPost.html', post=data)


# update post after sending form
@app.post("/edit/<id>")
def updatePost(id):

    newtitle = request.form.get('title')
    newdescription = request.form.get('description')
    newprice = request.form.get('price')

    addcom = ("UPDATE Posts \
                SET title = (%s), \
                description = (%s), \
                price = (%s) WHERE id = (%s)")

    addvals = (newtitle, newdescription, newprice, id)

    mysqlcursor.execute(addcom, addvals)

    return redirect('/homepage')

# delete post using POST request


@app.route('/delete/<id>', methods=['POST'])
def deletePost(id):
    deletecom = ("DELETE FROM Posts WHERE id = (%s)")
    deletevals = (id,)
    mysqlcursor.execute(deletecom, deletevals)
    mydb.commit()

    return redirect('/homepage')


if __name__ == "__main__":
    app.run()
