from app import app
import unittest
import uuid

def test_signup():
    # generate unique id for test user
    username = str(uuid.uuid4())
    usermail = username + "@gmail.com"

    # test1 = good
    response = app.test_client().post("/signup", data={
                "usermail": usermail, 
                "name": username, 
                "pass1": "Passw0rd!", 
                "pass2": "Passw0rd!",
                }, follow_redirects=True)

    # test2 = mismatch passwords
    response = app.test_client().post("/signup", data={
                "usermail": usermail, 
                "name": username, 
                "pass1": "Passw0rd!", 
                "pass2": "Different!",
                }, follow_redirects=True)

    # test3 = improper email
    response = app.test_client().post("/signup", data={
                "usermail": username, 
                "name": username, 
                "pass1": "Passw0rd!", 
                "pass2": "Passw0rd!",
                }, follow_redirects=True)
    
    mysqlcursor = app.mydb.cursor(buffered=True)
    query = f"DELETE FROM Users WHERE username={username}"
    mysqlcursor.execute()


def test_editpost(): 
    postid = str(uuid.uuid4())

    # connect to db and create post before editing
    mysqlcursor = app.mydb.cursor(buffered=True)
    addcom = "INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = (postid, title, description, file.filename, user, 0, 0)
    
    mysqlcursor.execute()
    mysqlcursor.close()


    # test1 = good
    response = app.test_client().post('/edit/1', data={
                "title": "test_title", 
                "description": "test_description",
            }, follow_redirects=True)
    

    mysqlcursor = app.mydb.cursor(buffered=True)
    
    query = f"DELETE FROM Posts WHERE postid={postid}"
    mysqlcursor.execute()