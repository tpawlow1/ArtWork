from app import app, mydb
import uuid



def test_signup():
    # generate unique id for test user
    username = "gh3ifmsdy"
    usermail = username + "@gmail.com"

    # test1 = good
    response = app.test_client().post("/signup", data={
                "usermail": usermail, 
                "name": username, 
                "pass1": "Passw0rd!", 
                "pass2": "Passw0rd!",
                }, follow_redirects=True)
    
    # make sure that the response is good, and that the user lands on homepage, where it greets them by username
    assert response.status_code == 200
    assert username in response.data.decode('utf-8')

    mysqlcursor = mydb.cursor(buffered=True)
    mysqlcursor.execute(f"SELECT * FROM Users WHERE `username`='{username}'")
    results = mysqlcursor.fetchall()

    # test user is now in user database after being created
    assert username, usermail in results

    mysqlcursor.close()

    # test2 = mismatch passwords
    response = app.test_client().post("/signup", data={
                "usermail": usermail, 
                "name": username, 
                "pass1": "Passw0rd!", 
                "pass2": "Different!",
                }, follow_redirects=True)
    
    # make sure good response, and that the user goes back to the landing page (for now)
    assert response.status_code == 200
    assert "This is the Landing Page" in response.data.decode('utf-8')


    # test3 = user already exists
    response = app.test_client().post("/signup", data={
                "usermail": usermail, 
                "name": username, 
                "pass1": "Passw0rd!", 
                "pass2": "Passw0rd!",
                }, follow_redirects=True)
    
    # make sure response is good, and that user is redirected to login page after entering an account that already exists
    assert response.status_code == 200
    assert "Login to ArtWork!" in response.data.decode('utf-8')

    
    mysqlcursor = mydb.cursor(buffered=True)
    query = f"DELETE FROM Users WHERE `username`='{username}'"
    mysqlcursor.execute(query)
    mydb.commit()
    mysqlcursor.close()


def test_editpost(): 
    postid = str(uuid.uuid4())

    # connect to db and create post before editing
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = (postid, 'testtitle', 'test_desc', 'bunny.jpg', 'sample', 0, 0)
    
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()
    mysqlcursor.close()


    # test1 = good
    response = app.test_client().post(f'/edit/{postid}', data={
                "title": "test_title", 
                "description": "test_description",
            })
    
    # not really a logged in user, so we need to check with database that the post was updated. 
    assert response.status_code == 302

    mysqlcursor = mydb.cursor(buffered=True)
    mysqlcursor.execute(f"SELECT * FROM Posts WHERE `id`='{postid}'")
    results = mysqlcursor.fetchall()

    assert "test_title", "test_description" in results

    # test 2 where no input is given
    response = app.test_client().post(f'/edit/{postid}', data={
                "title": "", 
                "description": "",
            })
    
    # should still redirect
    assert response.status_code == 302

    mysqlcursor = mydb.cursor(buffered=True)
    query = f"DELETE FROM Posts WHERE `id`='{postid}'"
    mysqlcursor.execute(query)
    mydb.commit()



test_signup()
test_editpost()