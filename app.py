from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'


UPLOAD_FOLDER = os.getcwd() + '\\static\images\\'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


mydb = mysql.connector.connect(
    host="localhost",
    user="sqluser",
    password="password",
    database="ArtWork"
)

mysqlcursor = mydb.cursor()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getposts():
    # sending all post entries to index to appear
    mysqlcursor.execute("SELECT * FROM Posts")
    data = mysqlcursor.fetchall()

    return render_template('index.html', data=data)


# get index
@app.get("/")
def index():
    # sending all post entries to index to appear
    mysqlcursor.execute("SELECT * FROM Posts")
    data = mysqlcursor.fetchall()

    return render_template('index.html', data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor = mydb.cursor()

            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                session['logged_in'] = True
                return redirect('/dashboard')
            else:
                return render_template('login.html', message='Invalid login credentials. Please try again.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return render_template('login.html', message='Database error. Please try again later.')

        finally:
            cursor.close()
            mydb.close()

    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html', message='You have successfully logged in')
    else:
        return redirect('/login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

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
    addcom = 'INSERT INTO Users VALUES (%s, %s, %s)'
    addvals = (username, email, userpass1)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()
    # send user back to homepage or sign in
    return render_template('index.html')

# get create post form


@app.get("/createpost")
def get_createPost():
    return render_template('createPost.html')

# upload post information and create post


@app.post('/createpost')
def createPost():
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
    addcom = 'INSERT INTO Posts VALUES (%s, %s, %s, %s, %s)'
    addvals = (postid, title, description, price, file.filename)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    return getposts()


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

    return getposts()

# delete post using POST request


@app.route('/delete/<id>', methods=['POST'])
def deletePost(id):
    deletecom = ("DELETE FROM Posts WHERE id = (%s)")
    deletevals = (id,)
    mysqlcursor.execute(deletecom, deletevals)
    mydb.commit()

    return getposts()
# get create post form


@app.get("/createpost")
def get_createPost():
    return render_template('createPost.html')

# upload post information and create post


@app.post('/createpost')
def createPost():
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
    addcom = 'INSERT INTO Posts VALUES (%s, %s, %s, %s, %s)'
    addvals = (postid, title, description, price, file.filename)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    return getposts()


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

    return getposts()

# delete post using POST request


@app.route('/delete/<id>', methods=['POST'])
def deletePost(id):
    deletecom = ("DELETE FROM Posts WHERE id = (%s)")
    deletevals = (id,)
    mysqlcursor.execute(deletecom, deletevals)
    mydb.commit()

    return getposts()


if __name__ == "__main__":
    app.run()
