from app import app, mydb
import uuid
from freezegun import freeze_time


def test_bid():
    auction_id = str(uuid.uuid4())
    client = app.test_client()

    # test 1 - bidding without repeat bidders

    # create an artist
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testartist', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create 3 non-artists
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser1', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser2', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser3', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create auction made by testartist
    addcom = "INSERT INTO Auctions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    addvals = (auction_id, 'testtitle',
               'testdesc', 'bunny.jpg', 'testartist', '2022-12-31 12:00:00', '2023-01-01 12:00:00', 1000.00, 0, None, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    freeze_time("2023-01-01 11:00:00")

    with client.session_transaction() as session:
        session['user'] = 'testuser1'

    response = client.post('/bid', data={
        "bid": 100.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    with client.session_transaction() as session:
        session['user'] = 'testuser2'

    response = client.post('/bid', data={
        "bid": 200.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    with client.session_transaction() as session:
        session['user'] = 'testuser3'

    response = client.post('/bid', data={
        "bid": 300.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    # checks to make sure bids were recorded in the database
    mysqlcursor.execute("SELECT * FROM Bids WHERE bidder='testuser1'")
    results = mysqlcursor.fetchone()

    assert 'testuser1', 100 in results

    mysqlcursor.execute("SELECT * FROM Bids WHERE bidder='testuser2'")
    results = mysqlcursor.fetchone()

    assert 'testuser2', 200 in results

    mysqlcursor.execute("SELECT * FROM Bids WHERE bidder='testuser3'")
    results = mysqlcursor.fetchone()

    assert 'testuser3', 300 in results

    # checks to make sure that money was taken out of the bidders' accounts
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser1'")
    results = mysqlcursor.fetchone()

    assert 'testuser1', 900.00 in results

    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser2'")
    results = mysqlcursor.fetchone()

    assert 'testuser2', 800.00 in results

    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser3'")
    results = mysqlcursor.fetchone()

    assert 'testuser3', 700.00 in results

    freeze_time("2023-01-01 13:00:00")

    # update auction status to expired
    with client.session_transaction() as session:
        session['user'] = 'testuser3'

    response = client.get('/auctionhouse')

    assert response.status_code == 200

    # check to see auction was expired
    mysqlcursor.execute(
        f"SELECT * FROM Auctions WHERE auction_id='{auction_id}'")
    results = mysqlcursor.fetchone()

    assert 1 in results

    # check if non-winners recieved their money back
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser1'")
    results = mysqlcursor.fetchone()

    assert 1000.00 in results

    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser2'")
    results = mysqlcursor.fetchone()

    assert 1000.00 in results

    # check that winner was still charged
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser3'")
    results = mysqlcursor.fetchone()

    assert 700.00 in results

    # check that artist is paid
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testartist'")
    results = mysqlcursor.fetchone()

    assert 300.00 in results

    mysqlcursor.execute(
        f"TRUNCATE TABLE Bids")
    mydb.commit()
    mysqlcursor.execute(
        f"TRUNCATE TABLE Auctions")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testartist'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser1'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser2'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser3'")
    mydb.commit()


def test_bid2():
    auction_id = str(uuid.uuid4())
    client = app.test_client()

    # test 2 - bidding with repeat bidder

    # create an artist
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testartist', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create 3 non-artists
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser1', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser2', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser3', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create auction made by testartist
    addcom = "INSERT INTO Auctions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    addvals = (auction_id, 'testtitle',
               'testdesc', 'bunny.jpg', 'testartist', '2022-12-31 12:00:00', '2023-01-01 12:00:00', 1000.00, 0, None, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    freeze_time("2023-01-01 11:00:00")

    with client.session_transaction() as session:
        session['user'] = 'testuser1'

    response = client.post('/bid', data={
        "bid": 100.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    with client.session_transaction() as session:
        session['user'] = 'testuser2'

    response = client.post('/bid', data={
        "bid": 200.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    with client.session_transaction() as session:
        session['user'] = 'testuser3'

    response = client.post('/bid', data={
        "bid": 300.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    # repeat bidder
    with client.session_transaction() as session:
        session['user'] = 'testuser1'

    response = client.post('/bid', data={
        "bid": 400.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    # checks to make sure bids were recorded in the database
    mysqlcursor.execute(
        "SELECT * FROM Bids WHERE bidder='testuser1' ORDER BY bid_amount")
    results = mysqlcursor.fetchone()

    assert 'testuser1', 100 in results

    mysqlcursor.execute(
        "SELECT * FROM Bids WHERE bidder='testuser1' ORDER BY bid_amount DESC")
    results = mysqlcursor.fetchone()

    assert 400 in results  # second bid from this user

    mysqlcursor.execute("SELECT * FROM Bids WHERE bidder='testuser2'")
    results = mysqlcursor.fetchone()

    assert 'testuser2', 200 in results

    mysqlcursor.execute("SELECT * FROM Bids WHERE bidder='testuser3'")
    results = mysqlcursor.fetchone()

    assert 'testuser3', 300 in results

    # checks to make sure that money was taken out of the bidders' accounts
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser1'")
    results = mysqlcursor.fetchone()

    assert 'testuser1', 500.00 in results

    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser2'")
    results = mysqlcursor.fetchone()

    assert 'testuser2', 800.00 in results

    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser3'")
    results = mysqlcursor.fetchone()

    assert 'testuser3', 700.00 in results

    freeze_time("2023-01-01 13:00:00")

    # update auction status to expired
    with client.session_transaction() as session:
        session['user'] = 'testuser3'

    response = client.get('/auctionhouse')

    assert response.status_code == 200

    # check to see auction was expired
    mysqlcursor.execute(
        f"SELECT * FROM Auctions WHERE auction_id='{auction_id}'")
    results = mysqlcursor.fetchone()

    assert 1 in results

    # check if non-winners recieved their money back
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser2'")
    results = mysqlcursor.fetchone()

    assert 1000.00 in results

    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser3'")
    results = mysqlcursor.fetchone()

    assert 1000.00 in results

    # check that winner was still charged
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser1'")
    results = mysqlcursor.fetchone()

    assert 600.00 in results

    # check that artist is paid
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testartist'")
    results = mysqlcursor.fetchone()

    assert 400.00 in results

    mysqlcursor.execute(
        f"TRUNCATE TABLE Bids")
    mydb.commit()
    mysqlcursor.execute(
        f"TRUNCATE TABLE Auctions")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testartist'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser1'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser2'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser3'")
    mydb.commit()


def test_bid3():
    auction_id = str(uuid.uuid4())
    client = app.test_client()

    # test 3 - bidding with insufficient funds

    # create an artist
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testartist', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create a non-artist
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser1', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 50.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create auction made by testartist
    addcom = "INSERT INTO Auctions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    addvals = (auction_id, 'testtitle',
               'testdesc', 'bunny.jpg', 'testartist', '2022-12-31 12:00:00', '2023-01-01 12:00:00', 1000.00, 0, None, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    freeze_time("2023-01-01 11:00:00")

    with client.session_transaction() as session:
        session['user'] = 'testuser1'

    response = client.post('/bid', data={
        "bid": 100.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    # checks to see bid was not recorded in the database
    mysqlcursor.execute(
        "SELECT * FROM Bids WHERE bidder='testuser1'")
    results = mysqlcursor.fetchone()

    assert results == None

    # checks to see that money was not taken out of the bidders' accounts
    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser1'")
    results = mysqlcursor.fetchone()

    assert 'testuser1', 50.00 in results

    freeze_time("2023-01-01 13:00:00")

    mysqlcursor.execute(
        f"TRUNCATE TABLE Bids")
    mydb.commit()
    mysqlcursor.execute(
        f"TRUNCATE TABLE Auctions")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testartist'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser1'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser2'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser3'")
    mydb.commit()
