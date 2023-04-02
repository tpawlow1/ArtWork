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

    '''# test3 = improper email
    response = app.test_client().post("/signup", data={
                "usermail": username, 
                "name": username, 
                "pass1": "Passw0rd!", 
                "pass2": "Passw0rd!",
                }, follow_redirects=True)'''
    
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
    response = app.test_client().post('/edit/1', data={
                "title": "test_title", 
                "description": "test_description",
            })
    
    
    assert response.status_code == 302
    

    mysqlcursor = mydb.cursor(buffered=True)
    
    query = f"DELETE FROM Posts WHERE `id`='{postid}'"
    mysqlcursor.execute(query)
    mydb.commit()



test_signup()
test_editpost()