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



