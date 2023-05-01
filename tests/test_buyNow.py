from app import app, mydb
import uuid


def test_editProfile():
    auction_id = str(uuid.uuid4())
    client = app.test_client()

    # test 1 - check that user is taken to auctionExpanded correctly

    # create a test artist
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testartist', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create an auction made by testartist
    addcom = "INSERT INTO Auctions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    addvals = (auction_id, 'testtitle',
               'testdesc', 'bunny.jpg', 'testartist', '2023-04-01 10:33:00', '2026-05-01 10:44:00', 100.00, 0, None, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testartist'

    response = client.get(
        f'/auctionExpand/{auction_id}', data={'button': 'clicked'})

    # make sure user is sent to auctionExpanded after clicking view button
    assert response.status_code == 200

    # test 2 - user clicks buyNow with proper funds in account

    # creates a non-artist user to use buyNow feature
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 200.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testuser'

    response = client.get(
        f'/buyNow/{auction_id}', data={'button': 'clicked'})

    assert response.status_code == 302

    # check that database updated testuser's Money
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser'")
    results = mysqlcursor.fetchone()

    assert 'testuser', 100.00 in results

    # check that database expired auction
    mysqlcursor.execute(
        f"SELECT isExpired FROM Auctions WHERE auction_id='{auction_id}'")
    results = mysqlcursor.fetchone()

    assert 1 in results

    # check that database updated testartist's Money
    mysqlcursor.execute(f"SELECT * FROM Users WHERE username='testartist'")
    results = mysqlcursor.fetchone()

    assert 'testartist', 100.00 in results

    mysqlcursor.execute(
        f"DELETE FROM Users WHERE username='testartist'")
    mydb.commit()
    mysqlcursor.execute(
        f"DELETE FROM Auctions WHERE auction_id = '{auction_id}'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser'")
    mydb.commit()

    # test 3 - user clicks buyNow without proper funds

    # create a test artist
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testartist', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create an auction made by testartist
    addcom = "INSERT INTO Auctions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    addvals = (auction_id, 'testtitle',
               'testdesc', 'bunny.jpg', 'testartist', '2023-04-01 10:33:00', '2026-05-01 10:44:00', 100.00, 0, None, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # creates a non-artist user to use buyNow feature
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 50.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    with client.session_transaction() as session:
        session['user'] = 'testuser'

    response = client.get(
        f'/buyNow/{auction_id}', data={'button': 'clicked'})

    assert response.status_code == 302

    # check that database did not update testuser's Money
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser'")
    results = mysqlcursor.fetchone()

    assert 'testuser', 50.00 in results

    # check that database does not expire auction
    mysqlcursor.execute(
        f"SELECT isExpired FROM Auctions WHERE auction_id='{auction_id}'")
    results = mysqlcursor.fetchone()

    assert 0 in results

    # check that database does not update testartist's Money
    mysqlcursor.execute(f"SELECT * FROM Users WHERE username='testartist'")
    results = mysqlcursor.fetchone()

    assert 'testartist', 0.00 in results

    mysqlcursor.execute(
        f"DELETE FROM Users WHERE username='testartist'")
    mydb.commit()
    mysqlcursor.execute(
        f"DELETE FROM Auctions WHERE auction_id = '{auction_id}'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser'")
    mydb.commit()
    