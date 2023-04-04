from app import app, mydb


def test_artistVerification():

    client = app.test_client()

    # connect to database and add a user w/out artist privilege
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals = ('testusername', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0)

    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testusername'

    response = client.post('/artistverify', data={'button': 'clicked'})
    assert response.status_code == 302

    mysqlcursor.execute("SELECT * FROM Users WHERE username = 'testusername'")
    results = mysqlcursor.fetchone()

    assert "testusername", "testemail" in results
    assert "testpassword", "testbio" in results
    assert 1 == results[-1]

    mysqlcursor.execute("DELETE FROM Users WHERE username = 'testusername'")
    mydb.commit()
    mysqlcursor.close()
