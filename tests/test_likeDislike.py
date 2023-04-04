from app import app, mydb
import uuid


def test_like():
    postid = str(uuid.uuid4())
    client = app.test_client()

    # test - liking a post

    # making a post and user

    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals = ('testusername', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = (postid, 'testtitle', 'testdescription',
               'spacecraft.jpg', 'testusername', 0, 0)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testusername'

    response = client.post(f'/like/{postid}', data={'button': 'clicked'})

    # not really a logged in user, so we need to check with database that the info was updated.
    assert response.status_code == 302

    mysqlcursor.execute(f"SELECT * FROM Posts WHERE id = '{postid}'")
    results = mysqlcursor.fetchone()

    assert postid in results
    assert results[-2] == 1
    assert results[-1] == 0

    mysqlcursor.execute(
        f"SELECT * FROM Post_Interactions WHERE pi_postID ='{postid}'")
    results = mysqlcursor.fetchone()

    assert postid, 'testusername' in results
    assert results[-2] == 1
    assert results[-1] == 0

    mysqlcursor.execute(
        f"DELETE FROM Post_Interactions WHERE pi_postID = '{postid}' AND pi_userID = 'testusername'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Posts WHERE id = '{postid}'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username = 'testusername'")
    mydb.commit()
    mysqlcursor.close()


def test_dislike():
    postid = str(uuid.uuid4())
    client = app.test_client()

    # test - disliking a post

    # making a post and user

    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals = ('testusername', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = (postid, 'testtitle', 'testdescription',
               'spacecraft.jpg', 'testusername', 0, 0)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testusername'

    response = client.post(f'/dislike/{postid}', data={'button': 'clicked'})

    # not really a logged in user, so we need to check with database that the info was updated.
    assert response.status_code == 302

    mysqlcursor.execute(f"SELECT * FROM Posts WHERE id = '{postid}'")
    results = mysqlcursor.fetchone()

    assert postid in results
    assert results[-2] == 0
    assert results[-1] == 1

    mysqlcursor.execute(
        f"SELECT * FROM Post_Interactions WHERE pi_postID ='{postid}'")
    results = mysqlcursor.fetchone()

    assert postid, 'testusername' in results
    assert results[-2] == 0
    assert results[-1] == 1

    mysqlcursor.execute(
        f"DELETE FROM Post_Interactions WHERE pi_postID = '{postid}' AND pi_userID = 'testusername'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Posts WHERE id = '{postid}'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username = 'testusername'")
    mydb.commit()
    mysqlcursor.close()
