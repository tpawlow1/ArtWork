from app import app, mydb


def test_editProfile():

    client = app.test_client()

    # connect to database and create user before editing
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals = ('testusername', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0)

    mysqlcursor.execute(addcom, addvals)
    mydb.commit()
    mysqlcursor.close()

    with client.session_transaction() as session:
        session['user'] = 'testusername'

    # test1 = everything is edited
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

    # # test 2 where no input is given
    # response = app.test_client().post(f'/edit/{postid}', data={
    #     "title": "",
    #     "description": "",
    # })

    # # should still redirect
    # assert response.status_code == 302

    # mysqlcursor = mydb.cursor(buffered=True)
    # query = f"DELETE FROM Posts WHERE `id`='{postid}'"
    # mysqlcursor.execute(query)
    # mydb.commit()
