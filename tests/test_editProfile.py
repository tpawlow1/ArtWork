from app import app, mydb
# from werkzeug.datastructures import FileStorage


def test_editProfile():

    client = app.test_client()

    # connect to database and create user before editing
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testusername', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)

    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testusername'

    # test1 = valid input
    response = client.post(f'/profile', data={
        "username": "edited_username",
        "email": "edited_email",
        "password": "edited_password",
        "bio": "edited_bio",
    })

    # not really a logged in user, so we need to check with database that the info was updated.
    assert response.status_code == 302

    mysqlcursor = mydb.cursor(buffered=True)
    mysqlcursor.execute(
        f"SELECT * FROM Users WHERE username = 'edited_username'")
    results = mysqlcursor.fetchall()

    assert "edited_username", "edited_email" in results
    assert "edited_pasword", "edited_bio" in results

    mysqlcursor.execute("DELETE FROM Users WHERE username = 'edited_username'")
    mydb.commit()
    mysqlcursor.close()

    # test 2 - when no username is entered
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testusername', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)

    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testusername'

    response = client.post(f'/profile', data={
        "username": "",
        "email": "edited_email",
        "password": "edited_password",
        "bio": "edited_bio",
    })

    # not really a logged in user, so we need to check with database that the info was updated.
    assert response.status_code == 302

    mysqlcursor = mydb.cursor(buffered=True)
    mysqlcursor.execute(
        f"SELECT * FROM Users WHERE email = 'edited_email'")
    results = mysqlcursor.fetchall()

    assert "testusername", "edited_email" in results
    assert "edited_pasword", "edited_bio" in results

    mysqlcursor.execute("DELETE FROM Users WHERE username = 'testusername'")
    mydb.commit()
    mysqlcursor.close()

    # test 3 - when you try to change your username to one that already exists
    # user 1
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals = ('user1', 'user1mail',
               'user1pass', 'user1bio', 'bunny.jpg', 0)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # user 2
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals = ('user2', 'user2mail',
               'user2pass', 'user2bio', 'bunny.jpg', 0)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'user1'

    response = client.post(f'/profile', data={
        "username": "user2",
        "email": "user1mail",
        "password": "user1pass",
        "bio": "user1bio",
    })

    # not really a logged in user, so we need to check with database that the info was updated.
    assert response.status_code == 302

    mysqlcursor = mydb.cursor(buffered=True)
    mysqlcursor.execute(
        f"SELECT * FROM Users WHERE email = 'user1mail'")
    results = mysqlcursor.fetchall()

    assert "user1", "user1mail" in results
    assert "user1pass", "user1bio" in results

    mysqlcursor.execute("DELETE FROM Users WHERE username = 'user1'")
    mydb.commit()
    mysqlcursor.execute("DELETE FROM Users WHERE username = 'user2'")
    mydb.commit()
    mysqlcursor.close()


# def test_editProfilePic():

#     # test 1 - valid input
#     client = app.test_client()

#     # connect to database and create user before editing
#     mysqlcursor = mydb.cursor(buffered=True)
#     addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
#     addvals = ('testusername', 'testemail',
#                'testpassword', 'testbio', 'bunny.jpg', 0)

#     mysqlcursor.execute(addcom, addvals)
#     mydb.commit()

#     with client.session_transaction() as session:
#         session['user'] = 'testusername'

#     with open('static/images/spacecraft.jpg', 'rb') as f:
#         file = FileStorage(f, filename='spacecraft.jpg')

#     response = client.post(f'/profile/pic', data={
#         'file': file,
#     })

#     # not really a logged in user, so we need to check with database that the info was updated.
#     assert response.status_code == 302

#     mysqlcursor = mydb.cursor(buffered=True)
#     mysqlcursor.execute(
#         f"SELECT * FROM Users WHERE username = 'testusername'")
#     results = mysqlcursor.fetchall()

#     assert "testusername", "testemail" in results
#     assert "testpassword", "testbio" in results
#     assert "spacecraft.jpg" in results

#     mysqlcursor.execute("DELETE FROM Users WHERE username = 'testusername'")
#     mydb.commit()
#     mysqlcursor.close()
