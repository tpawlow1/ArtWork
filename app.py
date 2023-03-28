from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os
import uuid
import datetime


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
    # sending all post entries to index to appear
    mysqlcursor.execute(f"SELECT * FROM Posts")
    data = mysqlcursor.fetchall()

    return data


def getauctions():
    mysqlcursor.execute(f"SELECT * FROM Auctions WHERE isExpired = 0")
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
    bio = 'Change me when you get a second!'
    propicpath = 'default_profilepic.jpg'

    # verify passwords match
    if userpass1 != userpass2:
        # placeholder bounce back if no match
        return render_template('index.html')
    # if all good, send to user table in database
    addcom = 'INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)'
    addvals = (username, email, userpass1, bio, propicpath, '0')
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
    return render_template("homepage.html", post=data, user=user)


@app.get("/profile")
def profilePage():
    user = session['user']
    mysqlcursor.execute(f"SELECT * FROM Users WHERE username='{user}'")
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
    addcom = 'INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)'
    addvals = (postid, title, description,
               file.filename, user, 0, 0)
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

    addcom = ("UPDATE Posts \
                SET title = (%s), \
                description = (%s) \
                 WHERE id = (%s)")

    addvals = (newtitle, newdescription, id)

    mysqlcursor.execute(addcom, addvals)

    return redirect('/homepage')

# send user to post page with comments, submit comment to db and reload page


@app.route('/comments/<id>', methods=['GET', 'POST'])
def getPostComments(id):

    # grabbing post info
    mysqlcursor.execute("SELECT * FROM Posts WHERE id = '" + str(id) + "'")
    data = mysqlcursor.fetchall()[0]

    if request.method == 'POST':
        # info from comment
        comment = request.form.get('comment')
        username = session['user']

        # add comment info to comment table
        addcom = 'INSERT INTO Comments VALUES (%s, %s, %s)'
        addvals = (id, comment, username)
        mysqlcursor.execute(addcom, addvals)
        mydb.commit()

     # grabbing comments info
    mysqlcursor.execute(
        "SELECT * FROM Comments WHERE post_id = '" + str(id) + "'")
    comments = mysqlcursor.fetchall()

    return render_template('postComments.html', post=data, comments=comments)


# delete post using POST request
@app.route('/delete/<id>', methods=['POST'])
def deletePost(id):
    deletecom = ("DELETE FROM Posts WHERE id = (%s)")
    deletevals = (id,)
    mysqlcursor.execute(deletecom, deletevals)
    mydb.commit()

    return redirect('/homepage')

# follow user


@app.post('/follow')
def follow_user():
    following = request.form.get('username')
    user = session['user']

    mysqlcursor.execute(
        f"SELECT * FROM Follows WHERE follower='{user}' AND following='{following}'")
    existing_relationship = mysqlcursor.fetchone()

    if existing_relationship is not None:
        return redirect(url_for('homepage'))

    addcom = 'INSERT INTO Follows (follower, following) VALUES (%s, %s)'
    addvals = (user, following)
    mysqlcursor.execute(addcom, addvals)

    mydb.commit()

    return redirect(url_for('homepage'))

# unfollow user


@app.post('/unfollow')
def unfollow_user():
    unfollowing = request.form.get('username')
    user = session['user']

    deletecom = f"DELETE FROM Follows WHERE follower='{user}' AND following='{unfollowing}'"
    mysqlcursor.execute(deletecom)

    mydb.commit()

    return redirect(url_for('homepage'))


@app.get("/msg/<uname>")
def chatuser(uname):
    return render_template('/msguser', user=uname)

# like post using POST request


@app.route('/like/<id>', methods=['POST'])
def like_post(id):
    likecom = ("UPDATE Posts SET likes = likes + 1 WHERE id = (%s)")
    likevals = (id,)
    mysqlcursor.execute(likecom, likevals)
    mydb.commit()

    likecom = ("UPDATE Posts SET dislikes = dislikes - 1 WHERE id = (%s)")
    likevals = (id,)
    mysqlcursor.execute(likecom, likevals)
    mydb.commit()

    return redirect('/homepage')

# dislike post using POST request


@app.route('/dislike/<id>', methods=['POST'])
def dislike_post(id):
    dislikecom = ("UPDATE Posts SET dislikes = dislikes + 1 WHERE id = (%s)")
    dislikevals = (id,)
    mysqlcursor.execute(dislikecom, dislikevals)
    mydb.commit()

    dislikecom = ("UPDATE Posts SET likes = likes - 1 WHERE id = (%s)")
    dislikevals = (id,)
    mysqlcursor.execute(dislikecom, dislikevals)
    mydb.commit()

    return redirect('/homepage')

# navigate to artist verification using GET method


@app.get("/artistverify")
def getArtistVerify():
    return render_template('artistverify.html')

# verify artist status using POST method


@app.post("/artistverify")
def verifyArtist():
    user = session['user']
    mysqlcursor.execute(
        f"UPDATE Users SET isArtist = true WHERE username = '{user}'")
    mydb.commit()
    return redirect('/profile')

# load auctionHouse.html with proper credentials with GET method


@app.get("/auctionhouse")
def getAuctionHouse():
    user = session['user']
    mysqlcursor.execute(f"SELECT * FROM Users WHERE username='{user}'")
    data = mysqlcursor.fetchall()

    # updates status of auctions whenever page is refreshed
    mysqlcursor.execute(
        "UPDATE Auctions SET isExpired = true WHERE NOW() > endTime;")
    auction = getauctions()
    return render_template("auctionHouse.html", data=data, auction=auction)

# creating an Auction post with the POST method


@app.post("/createAuction")
def createAuctionPost():
    user = session['user']
    # generate unique id
    auctionid = str(uuid.uuid4())

    # pull from post
    title = request.form.get('title')
    description = request.form.get('description')
    endDate = request.form.get('endDate')
    endTime = request.form.get('endTime')
    price = request.form.get('price')

    # formatting the date and time for MySQL
    endDate = endDate.split('/')
    auctionEnd = f'{endDate[2]}-{endDate[0]}-{endDate[1]} {endTime}:00'

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
    mysqlcursor.execute(
        f"INSERT INTO Auctions (auction_id, title, description, filepath, user, endTime, price, isExpired) VALUES ('{auctionid}', '{title}', '{description}', '{file.filename}', '{user}', '{auctionEnd}', '{price}', 0)")
    mydb.commit()
    return redirect('/auctionhouse')


if __name__ == "__main__":
    app.run()
